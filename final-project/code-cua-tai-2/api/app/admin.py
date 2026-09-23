from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from .db import get_db
from .models import Exercise, KnowledgeItem, KnowledgeRelation, User
from .security import admin_user

router = APIRouter(prefix='/api/v1/admin', tags=['admin'])

@router.get('/overview')
def overview(db: Session = Depends(get_db), _: User = Depends(admin_user)):
    return {
        'knowledge_items': db.scalar(select(func.count()).select_from(KnowledgeItem)) or 0,
        'relations': db.scalar(select(func.count()).select_from(KnowledgeRelation)) or 0,
        'exercises': db.scalar(select(func.count()).select_from(Exercise)) or 0,
        'users': db.scalar(select(func.count()).select_from(User)) or 0,
    }
