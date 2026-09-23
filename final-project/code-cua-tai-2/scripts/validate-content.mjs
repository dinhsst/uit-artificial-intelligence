import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(new URL('..', import.meta.url).pathname)
const read = name => JSON.parse(fs.readFileSync(path.join(root, 'content', name), 'utf8'))
const knowledge = read('knowledge.json')
const relations = read('relations.json')
const exercises = read('exercises.json')
const quizzes = read('quizzes.json')
const visualizations = read('visualizations.json')
const lessons = read('lessons.json')
const syllabus = read('syllabus.json')
const errors = []
const ids = new Set(knowledge.map(item => item.id))
const exerciseIds = new Set(exercises.map(item => item.id))
const visualizationIds = new Set(visualizations.map(item => item.id))
const lessonIds = new Set(lessons.map(item => item.id))
if (ids.size !== knowledge.length) errors.push('duplicate knowledge IDs')
for (const chapter of syllabus) for (const lesson of chapter.lessons) if (!lessonIds.has(lesson)) errors.push(`missing lesson: ${lesson}`)
for (const edge of relations) if (!ids.has(edge.sourceId) || !ids.has(edge.targetId)) errors.push(`broken relation: ${edge.sourceId} -> ${edge.targetId}`)
for (const exercise of exercises) {
  if (exercise.hints?.length !== 3) errors.push(`exercise must have 3 hints: ${exercise.id}`)
  for (const id of exercise.requiredKnowledge ?? []) if (!ids.has(id)) errors.push(`missing exercise knowledge: ${exercise.id} -> ${id}`)
  for (const id of exercise.patterns ?? []) if (!ids.has(id)) errors.push(`missing exercise pattern: ${exercise.id} -> ${id}`)
  for (const id of exercise.relatedExercises ?? []) if (!exerciseIds.has(id)) errors.push(`missing related exercise: ${exercise.id} -> ${id}`)
  if (exercise.visualizationId && !visualizationIds.has(exercise.visualizationId)) errors.push(`missing visualization: ${exercise.id} -> ${exercise.visualizationId}`)
}
for (const quiz of quizzes) {
  if (quiz.answer < 0 || quiz.answer >= quiz.options.length) errors.push(`invalid quiz answer: ${quiz.id}`)
  if (!ids.has(quiz.relatedKnowledge)) errors.push(`missing quiz knowledge: ${quiz.id}`)
}
for (const visualization of visualizations) if (!visualization.events?.length) errors.push(`visualization has no events: ${visualization.id}`)
if (errors.length) { console.error(errors.join('\n')); process.exit(1) }
console.log(`Content valid: ${knowledge.length} knowledge, ${lessons.length} lessons, ${relations.length} relations, ${exercises.length} exercises, ${quizzes.length} quizzes, ${visualizations.length} visualizations`)
