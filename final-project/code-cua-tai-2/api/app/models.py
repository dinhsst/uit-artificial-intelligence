from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    role: Mapped[str] = mapped_column(String(16), default='LEARNER')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class KnowledgeItem(Base):
    __tablename__ = 'knowledge_items'
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    type: Mapped[str] = mapped_column(String(32), index=True)
    title_vi: Mapped[str] = mapped_column(String(300))
    title_en: Mapped[str] = mapped_column(String(300))
    summary_vi: Mapped[str] = mapped_column(Text)
    summary_en: Mapped[str] = mapped_column(Text)
    definition_vi: Mapped[str] = mapped_column(Text)
    definition_en: Mapped[str] = mapped_column(Text)
    chapter_id: Mapped[str] = mapped_column(String(100), index=True)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    syntax: Mapped[str | None] = mapped_column(Text, nullable=True)

class KnowledgeRelation(Base):
    __tablename__ = 'knowledge_relations'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    source_id: Mapped[str] = mapped_column(ForeignKey('knowledge_items.id', ondelete='CASCADE'), index=True)
    target_id: Mapped[str] = mapped_column(ForeignKey('knowledge_items.id', ondelete='CASCADE'), index=True)
    relation_type: Mapped[str] = mapped_column(String(32), index=True)
    weight: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_json: Mapped[dict] = mapped_column('metadata', JSON, default=dict)
    __table_args__ = (UniqueConstraint('source_id', 'target_id', 'relation_type'),)

class Exercise(Base):
    __tablename__ = 'exercises'
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    title_vi: Mapped[str] = mapped_column(String(300))
    title_en: Mapped[str] = mapped_column(String(300))
    statement_vi: Mapped[str] = mapped_column(Text)
    statement_en: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[str] = mapped_column(String(16))
    tags: Mapped[list] = mapped_column(JSON, default=list)
    patterns: Mapped[list] = mapped_column(JSON, default=list)
    required_knowledge: Mapped[list] = mapped_column(JSON, default=list)
    strategy: Mapped[list] = mapped_column(JSON, default=list)
    pseudocode: Mapped[list] = mapped_column(JSON, default=list)
    hints: Mapped[list] = mapped_column(JSON, default=list)
    solution: Mapped[str] = mapped_column(Text)
    mistakes: Mapped[list] = mapped_column(JSON, default=list)
    visualization_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    related_exercises: Mapped[list] = mapped_column(JSON, default=list)

class UserProgress(Base):
    __tablename__ = 'user_progress'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    entity_type: Mapped[str] = mapped_column(String(32))
    entity_id: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(32))
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint('user_id', 'entity_type', 'entity_id'),)
