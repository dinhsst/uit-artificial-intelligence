from typing import Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class Localized(BaseModel):
    vi: str
    en: str

class KnowledgeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str; type: str; title: Localized; summary: Localized; definition: Localized; chapter_id: str; tags: list[str] = []; syntax: str | None = None

class RelationOut(BaseModel):
    source_id: str; target_id: str; relation_type: str; distance: int = 1

class GraphOut(BaseModel):
    node: KnowledgeOut
    neighbors: list[KnowledgeOut]
    relations: list[RelationOut]

class SearchOut(BaseModel):
    results: list[KnowledgeOut]
    query: str
    confidence: float
    fallback_available: bool

class ExerciseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str; title: Localized; statement: Localized; difficulty: str; tags: list[str]; patterns: list[str]; required_knowledge: list[str]; strategy: list[Any]; pseudocode: list[str]; hints: list[Any]; solution: str; mistakes: list[Any]; visualization_id: str | None; related_exercises: list[str]

class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=64, pattern=r'^[A-Za-z0-9_]+$')
    password: str = Field(min_length=8, max_length=128)

class LoginIn(RegisterIn): pass
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    username: str
    role: str
class TokenOut(BaseModel): access_token: str; token_type: str = 'bearer'; user: UserOut
class ProgressIn(BaseModel): entity_type: str = Field(min_length=1, max_length=32); entity_id: str = Field(min_length=1, max_length=100); status: str = Field(min_length=1, max_length=32); score: int | None = Field(default=None, ge=0, le=100)
class ProgressOut(ProgressIn): id: UUID; user_id: UUID

class CodeRunIn(BaseModel):
    code: str = Field(min_length=1, max_length=32000)
    stdin: str = Field(default='', max_length=8000)

class CodeRunOut(BaseModel):
    status: str
    stdout: str = ''
    stderr: str = ''
    exit_code: int | None = None
    trace_available: bool = False
    trace_message: str

class AIRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    context_ids: list[str] = Field(default_factory=list, max_length=12)

class AIResponse(BaseModel):
    text: str
    generated: bool
    sources: list[str]
    available: bool
