import { describe, expect, it } from 'vitest'
import { chapters, exercises, knowledge, lessons, quizzes, relations, validateContent, visualizations } from '../src/domain/content'

describe('canonical content pack', () => {
  it('contains the planned first content batch', () => {
    expect(chapters).toHaveLength(13)
    expect(lessons).toHaveLength(52)
    expect(knowledge.length).toBeGreaterThanOrEqual(30)
    expect(relations.length).toBeGreaterThanOrEqual(30)
    expect(exercises.length).toBeGreaterThanOrEqual(12)
    expect(quizzes.length).toBeGreaterThanOrEqual(20)
    expect(visualizations.length).toBeGreaterThanOrEqual(10)
  })

  it('has no broken content references', () => {
    expect(validateContent()).toEqual([])
    const lessonIds = new Set(lessons.map(lesson => lesson.id))
    expect(chapters.every(chapter => chapter.lessons.every(id => lessonIds.has(id)))).toBe(true)
  })

  it('keeps three progressive hints on every exercise', () => {
    expect(exercises.every(exercise => exercise.hints.length === 3)).toBe(true)
  })
})
