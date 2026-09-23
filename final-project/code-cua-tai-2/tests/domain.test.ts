import { describe, expect, it } from 'vitest'
import { exercises, knowledge, relations } from '../src/domain/content'
import { neighborhood, recommend } from '../src/domain/recommendations'
import { searchExercises, searchKnowledge } from '../src/domain/search'

describe('knowledge search', () => {
  it('finds the same topic with Vietnamese accents and no accents', () => {
    const accented = searchKnowledge('tìm số lớn nhất trong mảng', knowledge)
    const plain = searchKnowledge('tim max mang', knowledge)
    expect(accented[0]?.id).toBe('find-max')
    expect(plain.some(item => item.id === 'find-max')).toBe(true)
  })
  it('supports a natural-language synonym', () => {
    expect(searchKnowledge('lấy phần tử lớn nhất', knowledge)[0]?.id).toBe('find-max')
  })
  it('searches exercises without Vietnamese accents', () => {
    expect(searchExercises('tim gia tri lon nhat', exercises)[0]?.id).toBe('exercise-find-max')
  })
})

describe('knowledge graph', () => {
  it('returns a bounded neighborhood', () => {
    const nodes = neighborhood('find-max', knowledge, relations, 1, 4)
    expect(nodes.length).toBeLessThanOrEqual(4)
    expect(nodes.some(node => node.item.id === 'array' || node.item.id === 'maintain-best')).toBe(true)
  })
  it('explains recommendations without exposing internal scores', () => {
    const result = recommend('find-max', knowledge, relations)
    expect(result.some(item => item.item.id === 'for-loop' && item.reason.vi.length > 0)).toBe(true)
    expect(result[0]).not.toHaveProperty('score')
  })
})

describe('content contract', () => {
  it('keeps exercises linked to existing knowledge', () => {
    const ids = new Set(knowledge.map(item => item.id))
    expect(exercises.every(exercise => exercise.requiredKnowledge.every(id => ids.has(id)))).toBe(true)
  })
})
