import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Exercise, KnowledgeItem, KnowledgeRelation

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'

def load(name):
    return json.loads((CONTENT / name).read_text(encoding='utf-8'))

def content_data():
    knowledge = load('knowledge.json')
    relations = load('relations.json')
    exercises = load('exercises.json')
    return knowledge, relations, exercises

def validate():
    knowledge, relations, exercises = content_data()
    ids = {item['id'] for item in knowledge}
    exercise_ids = {item['id'] for item in exercises}
    errors = []
    if len(ids) != len(knowledge): errors.append('duplicate knowledge id')
    for edge in relations:
        if edge['sourceId'] not in ids or edge['targetId'] not in ids: errors.append(f"broken relation {edge['sourceId']} -> {edge['targetId']}")
    for exercise in exercises:
        if len(exercise.get('hints', [])) != 3: errors.append(f"exercise {exercise['id']} must have 3 hints")
        for item_id in exercise.get('requiredKnowledge', []):
            if item_id not in ids: errors.append(f"missing knowledge {item_id}")
        for exercise_id in exercise.get('relatedExercises', []):
            if exercise_id not in exercise_ids: errors.append(f"missing exercise {exercise_id}")
    if errors: raise SystemExit('\n'.join(errors))
    print(f'Content valid: {len(knowledge)} knowledge, {len(relations)} relations, {len(exercises)} exercises')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--validate', action='store_true')
    args = parser.parse_args()
    validate()
    if args.validate: return
    knowledge, relations, exercises = content_data()
    with SessionLocal() as db:
        for item in knowledge:
            data = {**item, 'title_vi': item['title']['vi'], 'title_en': item['title']['en'], 'summary_vi': item['summary']['vi'], 'summary_en': item['summary']['en'], 'definition_vi': item['definition']['vi'], 'definition_en': item['definition']['en'], 'chapter_id': item['chapterId'], 'syntax': item.get('syntax')}
            for key in ('title','summary','definition','chapterId','properties','example','mistakes','pattern','problemTypes'): data.pop(key, None)
            existing = db.get(KnowledgeItem, item['id'])
            if existing:
                for key, value in data.items(): setattr(existing, key, value)
            else: db.add(KnowledgeItem(**data))
        db.flush()
        for edge in relations:
            existing = db.scalar(select(KnowledgeRelation).where(KnowledgeRelation.source_id==edge['sourceId'], KnowledgeRelation.target_id==edge['targetId'], KnowledgeRelation.relation_type==edge['type']))
            if not existing: db.add(KnowledgeRelation(source_id=edge['sourceId'], target_id=edge['targetId'], relation_type=edge['type'], weight=edge.get('weight', 1), metadata_json={}))
        for item in exercises:
            data = {'id':item['id'], 'title_vi':item['title']['vi'], 'title_en':item['title']['en'], 'statement_vi':item['statement']['vi'], 'statement_en':item['statement']['en'], 'difficulty':item['difficulty'], 'tags':item.get('tags',[]), 'patterns':item.get('patterns',[]), 'required_knowledge':item.get('requiredKnowledge',[]), 'strategy':item.get('strategy',[]), 'pseudocode':item.get('pseudocode',[]), 'hints':item.get('hints',[]), 'solution':item['solution'], 'mistakes':item.get('mistakes',[]), 'visualization_id':item.get('visualizationId'), 'related_exercises':item.get('relatedExercises',[])}
            existing = db.get(Exercise, item['id'])
            if existing:
                for key, value in data.items(): setattr(existing, key, value)
            else: db.add(Exercise(**data))
        db.commit()
    print(f'Seeded {len(knowledge)} knowledge items, {len(relations)} relations, {len(exercises)} exercises')

if __name__ == '__main__': main()
