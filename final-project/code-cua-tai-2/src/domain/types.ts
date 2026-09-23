export type Locale = 'vi' | 'en'
export type KnowledgeType = 'CONCEPT' | 'PROPERTY' | 'RULE' | 'PATTERN' | 'ALGORITHM' | 'TECHNIQUE' | 'EXAMPLE' | 'COMMON_MISTAKE' | 'EXERCISE'
export type RelationType = 'PREREQUISITE' | 'RELATED' | 'NEXT' | 'SIMILAR' | 'PRACTICE' | 'PATTERN' | 'REQUIRES' | 'COMMON_MISTAKE'
export type Difficulty = 'BEGINNER' | 'EASY' | 'MEDIUM' | 'HARD'

export interface Localized { vi: string; en: string }
export interface Chapter { id: string; order: number; title: Localized; lessons: string[] }
export interface Lesson { id: string; chapterId: string; order: number; title: Localized; intro: Localized; why: Localized; steps: Localized[]; example: string; mistakes: Localized[]; check: Localized; takeaway: Localized }
export interface KnowledgeItem {
  id: string; type: KnowledgeType; title: Localized; summary: Localized; definition: Localized
  tags: string[]; chapterId: string; properties?: Localized[]; syntax?: string; example?: string
  mistakes?: Localized[]; pattern?: string; problemTypes?: string[]
}
export interface Relation { sourceId: string; targetId: string; type: RelationType; weight?: number }
export interface Exercise {
  id: string; title: Localized; statement: Localized; difficulty: Difficulty; tags: string[]
  problemTypes?: string[]; input?: Localized; output?: Localized; constraints?: string; examples?: { input: string; output: string }[]
  patterns: string[]; requiredKnowledge: string[]; prerequisites?: string[]; learningObjectives?: Localized[] | { vi: string[]; en: string[] }; strategy: Localized[]; pseudocode: string[]
  hints: Localized[]; solution: string; mistakes: Localized[]; visualizationId?: string
  relatedExercises: string[]
}
export interface QuizQuestion { id: string; question: Localized; options: Localized[]; answer: number; explanation: Localized; relatedKnowledge: string }
export interface TraceEvent { step: number; line: number; event: string; variables: Record<string, string | number>; array?: number[]; output?: string }
export interface Visualization { id: string; title: Localized; description: Localized; code: string; events: TraceEvent[] }
export interface Recommendation { item: KnowledgeItem; category: string; reason: Localized; distance: number }
export interface ProgressState { viewedTopics: string[]; viewedVisualizations: string[]; openedHints: string[]; openedSolutions: string[]; solvedExercises: string[]; quizScores: Record<string, number> }
