import type { Exercise, KnowledgeItem } from './types'

const API_BASE = (import.meta.env.VITE_API_URL as string | undefined) ?? ''

async function request<T>(path: string, init: RequestInit = {}): Promise<T | null> {
  if (!API_BASE) return null
  try {
    const controller = new AbortController()
    const timeout = window.setTimeout(() => controller.abort(), 2500)
    const response = await fetch(`${API_BASE}${path}`, { ...init, signal: controller.signal, headers: { Accept: 'application/json', ...(init.headers ?? {}) } })
    window.clearTimeout(timeout)
    if (!response.ok) return null
    return await response.json() as T
  } catch {
    return null
  }
}

export function apiSearch(query: string) { return request<{ results: KnowledgeItem[]; query: string; confidence: number; fallback_available: boolean }>(`/api/v1/search?q=${encodeURIComponent(query)}`) }
export function apiKnowledge(id: string) { return request<KnowledgeItem>(`/api/v1/knowledge/${encodeURIComponent(id)}`) }
export function apiExercise(id: string) { return request<Exercise>(`/api/v1/exercises/${encodeURIComponent(id)}`) }
export function apiRunCode(code: string, stdin: string) { return request<{status:string;stdout:string;stderr:string;exit_code:number|null;trace_available:boolean;trace_message:string}>('/api/v1/code/run', {method:'POST', body:JSON.stringify({code,stdin}), headers:{'Content-Type':'application/json'}}) }
