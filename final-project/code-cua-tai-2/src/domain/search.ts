import type { Exercise, KnowledgeItem } from './types'

export function normalize(value: string) {
  return value.toLocaleLowerCase('vi').replace(/đ/g, 'd').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9\s-]/g, ' ').replace(/\s+/g, ' ').trim()
}
function distance(a: string, b: string) { const matrix = Array.from({length:a.length+1},(_,i)=>[i,...Array(b.length).fill(0)]); for(let j=0;j<=b.length;j++) matrix[0][j]=j; for(let i=1;i<=a.length;i++) for(let j=1;j<=b.length;j++) matrix[i][j]=Math.min(matrix[i-1][j]+1,matrix[i][j-1]+1,matrix[i-1][j-1]+(a[i-1]===b[j-1]?0:1)); return matrix[a.length][b.length] }
function searchItems<T>(query: string, items: T[], fieldsFor: (item: T) => string[]) {
  const q=normalize(query); if(!q) return items
  const tokens=q.split(' ')
  return items.map(item=>{ const fields=fieldsFor(item).map(normalize); const haystack=fields.join(' '); let score=0; if(fields.slice(0,2).some(x=>x===q)) score+=100; if(fields.slice(0,2).some(x=>x.includes(q))) score+=55; score+=tokens.filter(t=>haystack.includes(t)).length*12; const closest=Math.min(...fields.map(x=>distance(q,x.slice(0,Math.max(q.length,x.length))))); if(closest<=2) score+=8; return {item,score} }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).map(x=>x.item)
}

export function searchKnowledge(query: string, items: KnowledgeItem[]) {
  return searchItems(query,items,item=>[item.title.vi,item.title.en,item.summary.vi,item.summary.en,...item.tags])
}

export function searchExercises(query: string, items: Exercise[]) {
  return searchItems(query,items,item=>[item.title.vi,item.title.en,item.statement.vi,item.statement.en,...item.tags,...(item.problemTypes??[]),...item.patterns])
}
