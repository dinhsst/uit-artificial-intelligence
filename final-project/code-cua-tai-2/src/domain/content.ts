import syllabusData from '../../content/syllabus.json'
import knowledgeData from '../../content/knowledge.json'
import relationsData from '../../content/relations.json'
import exercisesData from '../../content/exercises.json'
import quizzesData from '../../content/quizzes.json'
import visualizationsData from '../../content/visualizations.json'
import lessonsData from '../../content/lessons.json'
import type { Chapter, Exercise, KnowledgeItem, Lesson, QuizQuestion, Relation, Visualization } from './types'

export const chapters = syllabusData as Chapter[]
export const knowledge = knowledgeData as KnowledgeItem[]
export const relations = relationsData as Relation[]
export const exercises = exercisesData as Exercise[]
export const quizzes = quizzesData as QuizQuestion[]
export const visualizations = visualizationsData as Visualization[]
export const lessons = lessonsData as Lesson[]

export function getKnowledge(id: string) { return knowledge.find(item => item.id === id) }
export function getExercise(id: string) { return exercises.find(item => item.id === id) }
export function getVisualization(id: string) { return visualizations.find(item => item.id === id) }

export function validateContent() {
  const ids = new Set(knowledge.map(item => item.id))
  const exerciseIds = new Set(exercises.map(item => item.id))
  const visualizationIds = new Set(visualizations.map(item => item.id))
  const errors: string[] = []
  if (ids.size !== knowledge.length) errors.push('Duplicate knowledge ID')
  relations.forEach(edge => { if (!ids.has(edge.sourceId) || !ids.has(edge.targetId)) errors.push(`Broken relation: ${edge.sourceId} -> ${edge.targetId}`) })
  exercises.forEach(exercise => {
    if (exercise.hints.length !== 3) errors.push(`Exercise ${exercise.id} must have 3 hints`)
    exercise.requiredKnowledge.forEach(id => { if (!ids.has(id)) errors.push(`Missing required knowledge: ${exercise.id} -> ${id}`) })
    exercise.patterns.forEach(id => { if (!ids.has(id)) errors.push(`Missing pattern: ${exercise.id} -> ${id}`) })
    exercise.relatedExercises.forEach(id => { if (!exerciseIds.has(id)) errors.push(`Missing related exercise: ${exercise.id} -> ${id}`) })
    if (exercise.visualizationId && !visualizationIds.has(exercise.visualizationId)) errors.push(`Missing visualization: ${exercise.id} -> ${exercise.visualizationId}`)
  })
  quizzes.forEach(question => { if (question.answer < 0 || question.answer >= question.options.length) errors.push(`Invalid quiz answer: ${question.id}`); if (!ids.has(question.relatedKnowledge)) errors.push(`Missing quiz knowledge: ${question.id}`) })
  visualizations.forEach(viz => { if (!viz.events.length) errors.push(`Visualization has no events: ${viz.id}`) })
  return errors
}

const contentErrors = validateContent()
if (contentErrors.length && import.meta.env.DEV) console.warn('Content validation:', contentErrors)
