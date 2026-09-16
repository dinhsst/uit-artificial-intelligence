import { runQuery } from '../db/neo4j.js';
import { buildAdjacency } from '../algorithms/traversal.js';

export async function getConcept(id) {
  const records = await runQuery('MATCH (n:Concept {id:$id}) RETURN n', { id });
  return records[0]?.get('n').properties ?? null;
}

const sourceTypesFor = (type) => ({
  Property: ['TINH_CHAT', 'NGUYEN_LY', 'LOI'],
  Exercise: ['BT', 'DANG_BT', 'VI_DU'],
  Method: ['PP_GIAI', 'TT'],
  Concept: ['KHAI_NIEM', 'THUAT_TOAN']
}[type] || (type ? [type] : []));

export async function getConcepts({ lesson, type } = {}) {
  const sourceTypes = sourceTypesFor(type);
  const records = await runQuery(`MATCH (n:Concept)
    WHERE ($lesson = '' OR n.lesson = $lesson)
      AND (size($sourceTypes) = 0 OR n.sourceType IN $sourceTypes)
    RETURN n ORDER BY n.lesson, n.name`, { lesson: lesson || '', sourceTypes });
  return records.map((record) => record.get('n').properties);
}

export async function searchConcepts(query, { lesson = '', type = '' } = {}) {
  const sourceTypes = sourceTypesFor(type);
  const records = await runQuery(`MATCH (n:Concept)
    WHERE ($lesson = '' OR n.lesson = $lesson)
      AND (size($sourceTypes) = 0 OR n.sourceType IN $sourceTypes)
      AND (toLower(n.name) CONTAINS toLower($query)
       OR toLower(coalesce(n.description, '')) CONTAINS toLower($query)
       OR toLower(coalesce(n.quote, '')) CONTAINS toLower($query)
       OR any(phrase IN coalesce(n.keyphrases, []) WHERE toLower(phrase) CONTAINS toLower($query))
       OR any(alias IN coalesce(n.aliases, []) WHERE toLower(alias) CONTAINS toLower($query)))
    RETURN n ORDER BY CASE WHEN toLower(n.name) = toLower($query) THEN 0 ELSE 1 END, n.name LIMIT 30`, { query, lesson, sourceTypes });
  return records.map((record) => record.get('n').properties);
}

export async function getLessons(subjectId = 'subj_ai') {
  const records = await runQuery(`MATCH (s:Subject {id:$subjectId})-[:HAS_LESSON]->(l:Lesson)
    OPTIONAL MATCH (l)-[:INCLUDES]->(n:Concept)
    RETURN l.id AS id, l.title AS title, l.order AS order, count(n) AS conceptCount ORDER BY l.order, l.id`, { subjectId });
  return records.map((record) => ({ id: record.get('id'), title: record.get('title'), order: Number(record.get('order') ?? 0), conceptCount: Number(record.get('conceptCount')) }));
}

export async function getNodesForLesson(lesson) {
  const records = await runQuery('MATCH (l:Lesson {id:$lesson})-[:INCLUDES]->(n:Concept) RETURN n ORDER BY n.sourceType, n.name', { lesson });
  return records.map((record) => record.get('n').properties);
}

export async function getContentForConcept(id, sourceType) {
  const sourceTypes = Array.isArray(sourceType) ? sourceType : [sourceType];
  const isProperty = sourceTypes.every((type) => ['TINH_CHAT', 'NGUYEN_LY', 'LOI'].includes(type));
  const relation = isProperty ? 'HAS_PROPERTY' : 'APPLIED_IN';
  const label = isProperty ? 'Property' : 'Exercise';
  const records = await runQuery(`MATCH (concept:Concept {id:$id})-[:${relation}]->(n:${label})
    WHERE n.sourceType IN $sourceTypes
    RETURN n ORDER BY n.name`, { id, sourceTypes });
  return records.map((record) => record.get('n').properties);
}

export async function getDocuments({ lesson } = {}) {
  const records = await runQuery(`MATCH (d:Document)
    OPTIONAL MATCH (l:Lesson)-[:HAS_DOCUMENT]->(d)
    WHERE ($lesson = '' OR coalesce(l.id, d.lesson) = $lesson)
    RETURN d.id AS id, d.file AS file, d.format AS format, coalesce(l.id, d.lesson) AS lesson,
      d.units AS units, d.characters AS characters ORDER BY d.file`, { lesson: lesson || '' });
  return records.map((record) => record.toObject());
}

export async function getDocument(id) {
  const records = await runQuery(`MATCH (d:Document {id:$id})
    OPTIONAL MATCH (l:Lesson)-[:HAS_DOCUMENT]->(d)
    RETURN d, collect({id:l.id, title:l.title}) AS lessons`, { id });
  if (!records.length) return null;
  const document = records[0].get('d').properties;
  return { ...document, lessons: records[0].get('lessons').filter((lesson) => lesson.id) };
}

export async function getMethodsForExercise(id) {
  const records = await runQuery(`MATCH (exercise:Exercise {id:$id})-[:SOLVED_BY]->(n:Method)
    RETURN n ORDER BY n.name`, { id });
  return records.map((record) => record.get('n').properties);
}

export async function getEdges() {
  const records = await runQuery(`MATCH (a:Concept)-[r:REQUIRES]->(b:Concept)
    RETURN a.id AS from, b.id AS to, type(r) AS type, r.weight AS weight, r.confidence AS confidence, r.reason AS reason`);
  return records.map((record) => ({
    from: record.get('from'), to: record.get('to'), type: record.get('type'), weight: Number(record.get('weight') ?? 1),
    confidence: Number(record.get('confidence') ?? 0), reason: record.get('reason') ?? ''
  }));
}

export async function getRelatedEdges() {
  const records = await runQuery(`MATCH (a:Concept)-[r:RELATED_TO]->(b:Concept)
    RETURN a.id AS from, b.id AS to, type(r) AS type, r.score AS score, r.reason AS reason`);
  return records.map((record) => ({
    from: record.get('from'), to: record.get('to'), type: record.get('type'), score: Number(record.get('score') ?? 0), reason: record.get('reason') ?? ''
  }));
}

export async function getGraph() {
  const [nodes, edges, relatedEdges] = await Promise.all([getConcepts(), getEdges(), getRelatedEdges()]);
  return { nodes, edges: [...edges, ...relatedEdges] };
}

export async function getAdjacency(direction = 'forward') {
  return buildAdjacency(await getEdges(), direction);
}

export async function getPrerequisites(id, maxDepth) {
  return { concept: await getConcept(id), adjacency: await getAdjacency('forward'), maxDepth };
}

export async function createEdge({ from, to, weight, reason }) {
  const records = await runQuery(`MATCH (a:Concept {id:$from}), (b:Concept {id:$to})
    OPTIONAL MATCH (a)-[existing:REQUIRES]->(b)
    WITH a, b, existing
    WHERE existing IS NULL
    CREATE (a)-[:REQUIRES {weight:$weight, confidence:1, reason:$reason}]->(b)
    RETURN a.id AS from`, { from, to, weight, reason });
  if (!records.length) throw new Error('EDGE_EXISTS_OR_ENDPOINT_MISSING');
}

export async function updateEdge({ from, to, weight, reason }) {
  const records = await runQuery(`MATCH (a:Concept {id:$from})-[r:REQUIRES]->(b:Concept {id:$to})
    SET r.weight=$weight, r.reason=$reason RETURN r`, { from, to, weight, reason });
  if (!records.length) throw new Error('EDGE_NOT_FOUND');
}

export async function deleteEdge({ from, to }) {
  const records = await runQuery(`MATCH (a:Concept {id:$from})-[r:REQUIRES]->(b:Concept {id:$to})
    DELETE r RETURN count(r) AS deleted`, { from, to });
  if (!records.length || Number(records[0].get('deleted')) === 0) throw new Error('EDGE_NOT_FOUND');
}

export async function createNode(node) {
  const records = await runQuery(`OPTIONAL MATCH (existing:Concept {id:$id})
    WITH existing WHERE existing IS NULL
    CREATE (n:Concept {id:$id, name:$name, type:$type, sourceType:$sourceType,
      lesson:$lesson, description:$description, quote:$quote, keyphrases:$keyphrases, aliases:$aliases})
    RETURN n`, node);
  if (!records.length) throw new Error('NODE_EXISTS');
  return records[0].get('n').properties;
}

export async function updateNode(id, node) {
  const records = await runQuery(`MATCH (n:Concept {id:$id})
    SET n.name=$name, n.type=$type, n.sourceType=$sourceType, n.lesson=$lesson,
      n.description=$description, n.quote=$quote, n.keyphrases=$keyphrases, n.aliases=$aliases
    RETURN n`, { id, ...node });
  if (!records.length) throw new Error('NODE_NOT_FOUND');
  return records[0].get('n').properties;
}

export async function deleteNode(id) {
  const records = await runQuery(`MATCH (n:Concept {id:$id})
    DETACH DELETE n RETURN count(n) AS deleted`, { id });
  if (!records.length || Number(records[0].get('deleted')) === 0) throw new Error('NODE_NOT_FOUND');
}

export async function updateDocument(id, document) {
  const records = await runQuery(`MATCH (d:Document {id:$id})
    SET d.file=$file, d.format=$format, d.lesson=$lesson
    RETURN d`, { id, ...document });
  if (!records.length) throw new Error('DOCUMENT_NOT_FOUND');
  return records[0].get('d').properties;
}

export async function deleteDocument(id) {
  const records = await runQuery(`MATCH (d:Document {id:$id}) DELETE d RETURN count(d) AS deleted`, { id });
  if (!records.length || Number(records[0].get('deleted')) === 0) throw new Error('DOCUMENT_NOT_FOUND');
}
