import type { ProgressState } from './types'
const key='cpp-atlas-progress'
const empty=():ProgressState=>({viewedTopics:[],viewedVisualizations:[],openedHints:[],openedSolutions:[],solvedExercises:[],quizScores:{}})
export function loadProgress():ProgressState { try { const raw=localStorage.getItem(key); return raw?{...empty(),...JSON.parse(raw)}:empty() } catch { return empty() } }
export function saveProgress(state:ProgressState){localStorage.setItem(key,JSON.stringify(state))}
export function markProgress(field:keyof Omit<ProgressState,'quizScores'>,id:string){const state=loadProgress(); if(!state[field].includes(id)) state[field].push(id); saveProgress(state); return state}
export function recordQuiz(id:string,score:number){const state=loadProgress(); state.quizScores[id]=score; saveProgress(state); return state}
export function isLessonComplete(state:ProgressState,topicId:string,exerciseId:string,quizId:string){return state.viewedTopics.includes(topicId)&&state.viewedVisualizations.length>0&&state.solvedExercises.includes(exerciseId)&&(state.quizScores[quizId]??0)>=70}
