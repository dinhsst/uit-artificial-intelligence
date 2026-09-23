import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db import Base, get_db
from app.main import app
from app.models import Exercise, KnowledgeItem, KnowledgeRelation
from src_seed import KNOWLEDGE, RELATIONS, EXERCISES

engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
Base.metadata.create_all(engine)
with TestingSession() as db:
    for data in KNOWLEDGE: db.add(KnowledgeItem(**data))
    db.flush()
    for data in RELATIONS: db.add(KnowledgeRelation(**data))
    for data in EXERCISES: db.add(Exercise(**data))
    db.commit()

def override_db():
    db = TestingSession()
    try: yield db
    finally: db.close()
app.dependency_overrides[get_db] = override_db
client = TestClient(app)

def test_search_graph_and_exercise():
    search = client.get('/api/v1/search', params={'q': 'tim max mang'})
    assert search.status_code == 200
    assert search.json()['results'][0]['id'] == 'find-max'
    graph = client.get('/api/v1/knowledge/find-max/graph')
    assert graph.status_code == 200
    assert any(item['id'] == 'loop' for item in graph.json()['neighbors'])
    exercise = client.get('/api/v1/exercises/exercise-find-max')
    assert exercise.status_code == 200
    assert len(exercise.json()['hints']) == 3

def test_auth_and_progress_ownership():
    first = client.post('/api/v1/auth/register', json={'username':'learner_one','password':'safe-pass-123'})
    assert first.status_code == 201
    token = first.json()['access_token']
    headers={'Authorization':f'Bearer {token}'}
    saved = client.post('/api/v1/progress', headers=headers, json={'entity_type':'exercise','entity_id':'exercise-find-max','status':'SOLVED','score':100})
    assert saved.status_code == 200
    assert client.get('/api/v1/progress', headers=headers).json()[0]['entity_id'] == 'exercise-find-max'
    assert client.get('/api/v1/me', headers=headers).json()['username'] == 'learner_one'

def test_auth_validation_and_missing_token():
    assert client.post('/api/v1/auth/register', json={'username':'bad','password':'short'}).status_code == 422
    assert client.get('/api/v1/progress').status_code == 401
