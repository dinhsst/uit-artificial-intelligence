import logging
import time
from collections import defaultdict, deque
from time import monotonic
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from .config import get_settings
from .db import get_db
from .models import Exercise, KnowledgeItem, KnowledgeRelation, User, UserProgress
from .schemas import ExerciseOut, GraphOut, KnowledgeOut, Localized, LoginIn, ProgressIn, ProgressOut, SearchOut, TokenOut, RegisterIn, UserOut
from .security import create_token, current_user, hash_password, verify_password
from .ai import AIProviderError, configured_provider
from .code_runner import run_code
from .schemas import AIRequest, AIResponse, CodeRunIn, CodeRunOut
from .admin import router as admin_router

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger('cpp-atlas.api')
settings=get_settings()
app=FastAPI(title=settings.app_name, version='0.1.0')
_login_attempts: dict[str, deque[float]] = defaultdict(deque)
_LOGIN_WINDOW_SECONDS = 300
_LOGIN_MAX_ATTEMPTS = 10

def _allow_login(username: str) -> bool:
    now = monotonic()
    attempts = _login_attempts[username]
    while attempts and now - attempts[0] > _LOGIN_WINDOW_SECONDS:
        attempts.popleft()
    if len(attempts) >= _LOGIN_MAX_ATTEMPTS:
        return False
    attempts.append(now)
    return True
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(admin_router)

def knowledge_out(item: KnowledgeItem) -> KnowledgeOut:
    return KnowledgeOut(id=item.id,type=item.type,title=Localized(vi=item.title_vi,en=item.title_en),summary=Localized(vi=item.summary_vi,en=item.summary_en),definition=Localized(vi=item.definition_vi,en=item.definition_en),chapter_id=item.chapter_id,tags=item.tags or [],syntax=item.syntax)
def exercise_out(item: Exercise) -> ExerciseOut:
    return ExerciseOut(id=item.id,title=Localized(vi=item.title_vi,en=item.title_en),statement=Localized(vi=item.statement_vi,en=item.statement_en),difficulty=item.difficulty,tags=item.tags or [],patterns=item.patterns or [],required_knowledge=item.required_knowledge or [],strategy=item.strategy or [],pseudocode=item.pseudocode or [],hints=item.hints or [],solution=item.solution,mistakes=item.mistakes or [],visualization_id=item.visualization_id,related_exercises=item.related_exercises or [])

def normalize(q: str) -> str:
    import unicodedata
    value=unicodedata.normalize('NFD', q.lower().replace('đ','d')).encode('ascii','ignore').decode()
    return ' '.join(''.join(c if c.isalnum() or c.isspace() else ' ' for c in value).split())

@app.middleware('http')
async def request_log(request, call_next):
    start=time.perf_counter(); response=await call_next(request); logger.info('%s %s %s %.2fms',request.method,request.url.path,response.status_code,(time.perf_counter()-start)*1000); return response

@app.get('/healthz')
def healthz(): return {'status':'ok','service':'api'}
@app.get('/api/v1/knowledge', response_model=list[KnowledgeOut])
def list_knowledge(type: str|None=None, chapter: str|None=None, db: Session=Depends(get_db)):
    stmt=select(KnowledgeItem).order_by(KnowledgeItem.id)
    if type: stmt=stmt.where(KnowledgeItem.type==type.upper())
    if chapter: stmt=stmt.where(KnowledgeItem.chapter_id==chapter)
    return [knowledge_out(x) for x in db.scalars(stmt).all()]
@app.get('/api/v1/knowledge/{item_id}', response_model=KnowledgeOut)
def get_knowledge(item_id: str, db: Session=Depends(get_db)):
    item=db.get(KnowledgeItem,item_id)
    if not item: raise HTTPException(404,'Knowledge item not found')
    return knowledge_out(item)
@app.get('/api/v1/knowledge/{item_id}/graph', response_model=GraphOut)
def get_graph(item_id: str, depth: int=Query(1,ge=1,le=3), limit: int=Query(20,ge=1,le=100), db: Session=Depends(get_db)):
    root=db.get(KnowledgeItem,item_id)
    if not root: raise HTTPException(404,'Knowledge item not found')
    visited={item_id}; queue=[(item_id,0)]; neighbors=[]; relation_out=[]
    while queue and len(neighbors)<limit:
        node_id,distance=queue.pop(0)
        edges=db.scalars(select(KnowledgeRelation).where(KnowledgeRelation.is_active==True,or_(KnowledgeRelation.source_id==node_id,KnowledgeRelation.target_id==node_id))).all()
        for edge in edges:
            next_id=edge.target_id if edge.source_id==node_id else edge.source_id
            if next_id in visited: continue
            visited.add(next_id); next_distance=distance+1
            if next_distance<=depth:
                node=db.get(KnowledgeItem,next_id)
                if node: neighbors.append(knowledge_out(node)); relation_out.append({'source_id':edge.source_id,'target_id':edge.target_id,'relation_type':edge.relation_type,'distance':next_distance}); queue.append((next_id,next_distance))
    return {'node':knowledge_out(root),'neighbors':neighbors,'relations':relation_out}
@app.get('/api/v1/search', response_model=SearchOut)
def search(q: str=Query(min_length=1,max_length=200), db: Session=Depends(get_db)):
    normalized=normalize(q); tokens=normalized.split(); items=db.scalars(select(KnowledgeItem)).all(); ranked=[]
    for item in items:
        fields=[normalize(item.title_vi),normalize(item.title_en),normalize(item.summary_vi),normalize(item.summary_en),*(normalize(tag) for tag in item.tags or [])]; hay=' '.join(fields); score=0
        if normalized in fields[:2]: score+=100
        if any(normalized in field for field in fields[:2]): score+=50
        score+=sum(12 for token in tokens if token in hay)
        if score: ranked.append((score,item))
    ranked.sort(key=lambda pair:(-pair[0],pair[1].id)); top=[knowledge_out(item) for _,item in ranked[:30]]; confidence=min(1.0,(ranked[0][0]/100) if ranked else 0)
    return {'results':top,'query':q,'confidence':confidence,'fallback_available':confidence<0.45}
@app.get('/api/v1/exercises', response_model=list[ExerciseOut])
def list_exercises(db: Session=Depends(get_db)): return [exercise_out(x) for x in db.scalars(select(Exercise).order_by(Exercise.id)).all()]
@app.get('/api/v1/exercises/{exercise_id}', response_model=ExerciseOut)
def get_exercise(exercise_id: str, db: Session=Depends(get_db)):
    exercise=db.get(Exercise,exercise_id)
    if not exercise: raise HTTPException(404,'Exercise not found')
    return exercise_out(exercise)
@app.post('/api/v1/auth/register', response_model=TokenOut, status_code=201)
def register(payload: RegisterIn, db: Session=Depends(get_db)):
    if db.scalar(select(User).where(User.username==payload.username)): raise HTTPException(409,'Username already exists')
    user=User(username=payload.username,password_hash=hash_password(payload.password)); db.add(user); db.commit(); db.refresh(user); return {'access_token':create_token(user),'user':user}
@app.post('/api/v1/auth/login', response_model=TokenOut)
def login(payload: LoginIn, db: Session=Depends(get_db)):
    if not _allow_login(payload.username):
        raise HTTPException(429, 'Too many login attempts; try again later')
    user=db.scalar(select(User).where(User.username==payload.username))
    if not user or not user.is_active or not verify_password(payload.password,user.password_hash): raise HTTPException(401,'Invalid username or password')
    return {'access_token':create_token(user),'user':user}
@app.get('/api/v1/me', response_model=UserOut)
def me(user: User=Depends(current_user)): return user
@app.get('/api/v1/progress', response_model=list[ProgressOut])
def list_progress(user: User=Depends(current_user), db: Session=Depends(get_db)): return db.scalars(select(UserProgress).where(UserProgress.user_id==user.id).order_by(UserProgress.created_at.desc())).all()
@app.post('/api/v1/progress', response_model=ProgressOut)
def set_progress(payload: ProgressIn, user: User=Depends(current_user), db: Session=Depends(get_db)):
    progress=db.scalar(select(UserProgress).where(UserProgress.user_id==user.id,UserProgress.entity_type==payload.entity_type,UserProgress.entity_id==payload.entity_id))
    if progress: progress.status=payload.status; progress.score=payload.score
    else: progress=UserProgress(user_id=user.id,**payload.model_dump()); db.add(progress)
    db.commit(); db.refresh(progress); return progress

@app.post('/api/v1/code/run', response_model=CodeRunOut)
async def code_run(payload: CodeRunIn, user: User=Depends(current_user)):
    result=await run_code(payload.code, payload.stdin)
    return result.__dict__

@app.post('/api/v1/ai/ask', response_model=AIResponse)
async def ai_ask(payload: AIRequest, db: Session=Depends(get_db), user: User=Depends(current_user)):
    source_items=[]
    for item_id in payload.context_ids:
        item=db.get(KnowledgeItem,item_id)
        if item: source_items.append(f'{item.id}: {item.title_vi} — {item.summary_vi}')
    provider=configured_provider()
    if provider is None:
        return {'text':'AI chưa được cấu hình. Knowledge Base và các công cụ học tập vẫn hoạt động độc lập.','generated':False,'sources':[item.split(':',1)[0] for item in source_items],'available':False}
    try:
        response=await provider.complete(payload.prompt, source_items)
    except AIProviderError:
        logger.warning('AI provider unavailable')
        return {'text':'AI tạm thời không khả dụng. Vui lòng thử lại sau.','generated':False,'sources':[item.split(':',1)[0] for item in source_items],'available':False}
    return {'text':response.text,'generated':response.generated,'sources':[item.split(':',1)[0] for item in source_items],'available':True}
