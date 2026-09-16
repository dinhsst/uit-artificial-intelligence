import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { driver } from './db/neo4j.js';
import { initializeSchema, closeDatabase } from './db/initialize.js';
import { config } from './config.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const source = JSON.parse(await fs.readFile(path.join(root, 'data/normalized-knowledge-base.json'), 'utf8'));
const extractedPath = path.join(root, 'data/rawdata-extracted.jsonl');
const documents = await fs.readFile(extractedPath, 'utf8').then((text) => text.split(/\r?\n/).filter(Boolean).map((line) => JSON.parse(line))).catch(() => []);
const mappingPath = path.join(root, 'knowledge-base/content-mappings.json');
const contentMappings = await fs.readFile(mappingPath, 'utf8').then((text) => JSON.parse(text).mappings || []).catch(() => []);
const typedLabels = ['Property', 'Exercise', 'Method'];
const lessonNames = { B1: 'Tổng quan về Trí tuệ nhân tạo', B2: 'Thuật giải Heuristic', B3: 'Không gian trạng thái & Phương pháp tìm kiếm', B4: 'Chiến lược Minimax', B5: 'Tổng quan về Biểu diễn tri thức', B6a: 'Các phương pháp biểu diễn tri thức cơ bản' };
const sourceTypeToLabel = {
  TINH_CHAT: 'Property', NGUYEN_LY: 'Property', LOI: 'Property',
  PP_GIAI: 'Method', TT: 'Method',
  BT: 'Exercise', DANG_BT: 'Exercise', VI_DU: 'Exercise'
};
const nodesByLabel = new Map([
  ['Property', []], ['Exercise', []], ['Method', []]
]);
for (const node of source.nodes) {
  const label = sourceTypeToLabel[node.sourceType];
  if (label) nodesByLabel.get(label).push(node);
}

const session = driver.session({ database: config.neo4jDatabase });
try {
  await initializeSchema();
  await session.executeWrite((tx) => tx.run(`UNWIND $nodes AS item
    MERGE (n:Concept {id:item.id})
    SET n.name=item.name, n.type=item.type, n.sourceType=item.sourceType,
        n.lesson=item.lesson, n.source=item.source, n.quote=item.quote,
        n.description=item.description, n.keyphrases=item.keyphrases, n.aliases=item.aliases`, { nodes: source.nodes }));
  await session.executeWrite((tx) => tx.run(`MERGE (s:Subject {id:'subj_ai'}) SET s.name='Trí tuệ nhân tạo', s.description='Môn học Trí tuệ nhân tạo'`));
  await session.executeWrite((tx) => tx.run(`UNWIND $lessons AS item
    MERGE (l:Lesson {id:item.id}) SET l.title=item.title, l.order=item.order
    WITH l MATCH (s:Subject {id:'subj_ai'}) MERGE (s)-[:HAS_LESSON]->(l)`, {
    lessons: Object.entries(lessonNames).map(([id, title], index) => ({ id, title, order: index + 1 }))
  }));
  await session.executeWrite((tx) => tx.run(`UNWIND $nodes AS item
    MATCH (n:Concept {id:item.id}), (l:Lesson {id:item.lesson})
    MERGE (l)-[:INCLUDES]->(n)`, { nodes: source.nodes.filter((node) => lessonNames[node.lesson]) }));
  if (documents.length) await session.executeWrite((tx) => tx.run(`UNWIND $documents AS item
    MERGE (d:Document {id:item.id})
    SET d.file=item.file, d.format=item.format, d.lesson=item.lesson,
        d.units=item.units, d.characters=item.characters, d.text=item.text
    WITH d, item
    OPTIONAL MATCH (l:Lesson {id:item.lesson})
    FOREACH (_ IN CASE WHEN l IS NULL THEN [] ELSE [1] END | MERGE (l)-[:HAS_DOCUMENT]->(d))`, { documents }));
  for (const label of typedLabels) {
    await session.executeWrite((tx) => tx.run(`MATCH (n:Concept) REMOVE n:${label}`));
    const nodes = nodesByLabel.get(label);
    if (nodes.length) await session.executeWrite((tx) => tx.run(`UNWIND $nodes AS item MATCH (n:Concept {id:item.id}) SET n:${label}`, { nodes }));
  }
  await session.executeWrite((tx) => tx.run(`MATCH (:Concept)-[r:REQUIRES]->(:Concept) DELETE r`));
  const conceptEdges = source.edges.filter((edge) => {
    const from = source.nodes.find((node) => node.id === edge.from);
    const to = source.nodes.find((node) => node.id === edge.to);
    return from?.entityKind === 'Concept' && to?.entityKind === 'Concept';
  });
  const edgeResult = await session.executeWrite((tx) => tx.run(`UNWIND $edges AS item
    MATCH (a:Concept {id:item.from}), (b:Concept {id:item.to})
    MERGE (a)-[r:REQUIRES]->(b)
    SET r.weight=item.weight, r.confidence=item.confidence, r.reason=item.reason,
        r.sourceRelationType=item.sourceRelationType, r.sourceIndex=item.sourceIndex
    RETURN count(r) AS importedEdges`, { edges: conceptEdges }));
  const importedEdges = edgeResult.records[0]?.get('importedEdges')?.toNumber?.() ?? conceptEdges.length;
  await session.executeWrite((tx) => tx.run(`MATCH (:Concept)-[r:HAS_PROPERTY|APPLIED_IN|INCLUDES|RELATED_TO]->() DELETE r`));
  await session.executeWrite((tx) => tx.run(`MATCH (:Exercise)-[r:SOLVED_BY]->() DELETE r`));
  if (source.relatedEdges?.length) await session.executeWrite((tx) => tx.run(`UNWIND $edges AS item
    MATCH (from:Concept {id:item.from}), (to:Concept {id:item.to})
    MERGE (from)-[r:RELATED_TO]->(to)
    SET r.score=item.score, r.reason=item.reason, r.sourceIndex=item.sourceIndex`, { edges: source.relatedEdges }));
  for (const relation of ['HAS_PROPERTY', 'APPLIED_IN', 'SOLVED_BY', 'INCLUDES']) {
    const mappings = contentMappings.filter((item) => item.relation === relation);
    if (mappings.length) await session.executeWrite((tx) => tx.run(`UNWIND $mappings AS item
      MATCH (from:Concept {id:item.from}), (to:Concept {id:item.to})
      MERGE (from)-[r:${relation}]->(to)
      SET r.reason=item.reason, r.provenance='curated_mapping'`, { mappings }));
  }
  console.log(JSON.stringify({ importedNodes: source.nodes.length, importedEdges, contentMappings: contentMappings.length, labels: Object.fromEntries([...nodesByLabel].map(([label, nodes]) => [label, nodes.length])) }));
} finally { await session.close(); await closeDatabase(); }
