import type { KnowledgeItem, Relation, Recommendation } from './types'

export function neighborhood(startId: string, items: KnowledgeItem[], relations: Relation[], maxDepth=2, maxNodes=12) {
  const byId=new Map(items.map(item=>[item.id,item])); const visited=new Set([startId]); const queue=[{id:startId,depth:0}]; const result:{item:KnowledgeItem; relation:Relation; distance:number}[]=[]
  while(queue.length && result.length<maxNodes){ const current=queue.shift()!; for(const relation of relations.filter(edge=>edge.sourceId===current.id || edge.targetId===current.id)){ const next=relation.sourceId===current.id?relation.targetId:relation.sourceId; if(visited.has(next)) continue; visited.add(next); const depth=current.depth+1; if(depth<=maxDepth){ const item=byId.get(next); if(item && result.length<maxNodes) result.push({item,relation,distance:depth}); if(result.length<maxNodes) queue.push({id:next,depth}) } } }
  return result
}
const labels: Record<string,string>={PREREQUISITE:'Nên biết trước',REQUIRES:'Nên biết trước',NEXT:'Học tiếp',RELATED:'Kiến thức liên quan',SIMILAR:'Kiến thức tương tự',PATTERN:'Phương pháp liên quan',PRACTICE:'Dạng bài áp dụng',COMMON_MISTAKE:'Lỗi thường gặp'}
export function recommend(startId:string,items:KnowledgeItem[],relations:Relation[],locale:'vi'|'en'='vi',enabled=true):Recommendation[]{
  if(!enabled) return relations.filter(r=>r.sourceId===startId).map(r=>{const item=items.find(i=>i.id===r.targetId)!;return {item,category:labels[r.type]??'Liên quan',distance:1,reason:{vi:`Liên kết trực tiếp với ${items.find(i=>i.id===startId)?.title.vi}.`,en:`Directly linked to ${items.find(i=>i.id===startId)?.title.en}.`}}})
  return neighborhood(startId,items,relations).map(({item,relation,distance})=>({item,distance,category:labels[relation.type]??'Liên quan',reason:{vi:`${item.title.vi} được gợi ý qua quan hệ ${labels[relation.type]??'liên quan'} trong bản đồ kiến thức.`,en:`${item.title.en} is suggested through a ${labels[relation.type]??'related'} relationship in the knowledge map.`}}))
}
