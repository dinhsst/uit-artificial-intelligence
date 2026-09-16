import express from 'express';
import { dfsTraverse, bfsTraverse, dijkstra, aStar, detectCycle } from '../algorithms/traversal.js';
import { getConcept, getConcepts, searchConcepts, getLessons, getNodesForLesson, getContentForConcept, getMethodsForExercise, getDocuments, getDocument, getEdges, getGraph, getAdjacency, createEdge, updateEdge, deleteEdge, createNode, updateNode, deleteNode, updateDocument, deleteDocument } from '../services/graphService.js';
import { authenticate, getMastery, issueToken, register, updateMastery } from '../services/authService.js';
import { answerWithGraph } from '../llm/graphRag.js';
import { requireAuth, requireRole } from '../middleware/auth.js';

const router = express.Router();
const finiteDepth = (value, fallback = 5) => {
  const depth = Number(value ?? fallback);
  return Number.isInteger(depth) && depth >= 0 && depth <= 100 ? depth : null;
};
const requireId = async (res, id) => {
  const concept = await getConcept(id);
  if (!concept) { res.status(404).json({ error: 'Không tìm thấy khái niệm.' }); return null; }
  return concept;
};

router.get('/health', (_req, res) => res.json({ status: 'ok' }));
router.post('/auth/register', async (req, res, next) => {
  try {
    const { name, email, password } = req.body;
    if (!name || !email || typeof password !== 'string' || password.length < 8) return res.status(400).json({ error: 'Tên, email và mật khẩu tối thiểu 8 ký tự là bắt buộc.' });
    const user = await register({ name, email, password });
    res.status(201).json({ user, token: issueToken(user) });
  } catch (error) { if (error.message === 'EMAIL_EXISTS' || error.code === 'Neo.ClientError.Schema.ConstraintValidationFailed') return res.status(409).json({ error: 'Email đã được sử dụng.' }); next(error); }
});
router.post('/auth/login', async (req, res, next) => {
  try {
    const user = await authenticate(req.body);
    if (!user) return res.status(401).json({ error: 'Email hoặc mật khẩu không đúng.' });
    res.json({ user, token: issueToken(user) });
  } catch (error) { next(error); }
});

router.get('/concepts', async (req, res, next) => { try { res.json(await getConcepts(req.query)); } catch (error) { next(error); } });
router.get('/concepts/:id', async (req, res, next) => { try { const concept = await requireId(res, req.params.id); if (concept) res.json(concept); } catch (error) { next(error); } });
router.get('/subjects/:subjectId/lessons', async (req, res, next) => { try { res.json(await getLessons(req.params.subjectId)); } catch (error) { next(error); } });
router.get('/lessons/:lessonId/concepts', async (req, res, next) => { try { res.json(await getNodesForLesson(req.params.lessonId)); } catch (error) { next(error); } });
router.get('/concepts/:id/properties', async (req, res, next) => { try { if (!await requireId(res, req.params.id)) return; res.json(await getContentForConcept(req.params.id, ['TINH_CHAT', 'NGUYEN_LY', 'LOI'])); } catch (error) { next(error); } });
router.get('/concepts/:id/exercises', async (req, res, next) => { try { if (!await requireId(res, req.params.id)) return; res.json(await getContentForConcept(req.params.id, ['BT', 'DANG_BT', 'VI_DU'])); } catch (error) { next(error); } });
router.get('/exercises/:id/methods', async (req, res, next) => { try { const exercise = await getConcept(req.params.id); if (!exercise || !['DANG_BT', 'VI_DU', 'BT'].includes(exercise.sourceType)) return res.status(404).json({ error: 'Không tìm thấy bài tập.' }); res.json(await getMethodsForExercise(req.params.id)); } catch (error) { next(error); } });
router.get('/search', async (req, res, next) => { try { const query = String(req.query.q || '').trim(); if (!query) return res.json([]); res.json(await searchConcepts(query, { lesson: String(req.query.lesson || ''), type: String(req.query.type || '') })); } catch (error) { next(error); } });
router.get('/graph', async (_req, res, next) => { try { res.json(await getGraph()); } catch (error) { next(error); } });
router.get('/documents', async (req, res, next) => { try { res.json(await getDocuments({ lesson: String(req.query.lesson || '') })); } catch (error) { next(error); } });
router.get('/documents/:id', async (req, res, next) => { try { const document = await getDocument(req.params.id); if (!document) return res.status(404).json({ error: 'Không tìm thấy tài liệu.' }); res.json(document); } catch (error) { next(error); } });
router.get('/concepts/:id/related', async (req, res, next) => {
  try {
    if (!await requireId(res, req.params.id)) return;
    const depth = finiteDepth(req.query.max_depth); if (depth === null) return res.status(400).json({ error: 'max_depth phải là số nguyên từ 0 đến 100.' });
    const adjacency = await getAdjacency('forward');
    const algorithm = req.query.algorithm || 'bfs';
    if (algorithm === 'dfs') return res.json(dfsTraverse(req.params.id, adjacency, depth));
    if (algorithm === 'bfs') return res.json(bfsTraverse(req.params.id, adjacency, depth));
    return res.status(400).json({ error: 'related chỉ hỗ trợ dfs hoặc bfs.' });
  } catch (error) { next(error); }
});
router.get('/concepts/:id/path', requireAuth, async (req, res, next) => {
  try {
    if (!await requireId(res, req.params.id)) return;
    if (!await requireId(res, req.query.target)) return;
    const depth = finiteDepth(req.query.max_depth, 100); if (depth === null) return res.status(400).json({ error: 'max_depth không hợp lệ.' });
    const algorithm = req.query.algorithm || 'dijkstra';
    const adjacency = await getAdjacency('reverse');
    if (algorithm === 'dijkstra') return res.json(dijkstra(req.params.id, req.query.target, adjacency, depth));
    if (algorithm === 'astar') return res.json(aStar(req.params.id, req.query.target, adjacency, await getMastery(req.user.sub), depth));
    return res.status(400).json({ error: 'path chỉ hỗ trợ dijkstra hoặc astar.' });
  } catch (error) { next(error); }
});
router.get('/users/me/progress', requireAuth, async (req, res, next) => { try { res.json(Object.fromEntries(await getMastery(req.user.sub))); } catch (error) { next(error); } });
router.put('/users/me/progress/:conceptId', requireAuth, async (req, res, next) => {
  try {
    if (!await requireId(res, req.params.conceptId)) return;
    const mastery = Number(req.body.mastery); if (!Number.isFinite(mastery) || mastery < 0 || mastery > 1) return res.status(400).json({ error: 'mastery phải nằm trong khoảng 0 đến 1.' });
    res.json(await updateMastery(req.user.sub, req.params.conceptId, mastery));
  } catch (error) { next(error); }
});
router.post('/ask', requireAuth, async (req, res, next) => {
  try {
    const question = String(req.body.question || '').trim(); if (!question) return res.status(400).json({ error: 'Câu hỏi không được để trống.' });
    const conceptId = String(req.body.conceptId || '').trim(); if (!conceptId || !await requireId(res, conceptId)) return;
    const traversal = bfsTraverse(conceptId, await getAdjacency('forward'), 3);
    const graph = await getGraph(); const ids = new Set(traversal.visited_order.map((item) => item.id));
    const subgraph = { nodes: graph.nodes.filter((node) => ids.has(node.id)), edges: graph.edges.filter((edge) => edge.type === 'REQUIRES' && ids.has(edge.from) && ids.has(edge.to)) };
    try { return res.json({ answer: await answerWithGraph({ question, subgraph }), traversal: traversal.visited_order }); }
    catch (error) { if (error.message === 'LLM_NOT_CONFIGURED' || error.name === 'APIConnectionError' || error.name === 'TimeoutError') return res.json({ fallback: true, answer: 'Chưa thể gọi mô hình; đây là các kiến thức liên quan được tìm thấy.', traversal: traversal.visited_order, subgraph }); throw error; }
  } catch (error) { next(error); }
});

const admin = [requireAuth, requireRole('ADMIN')];
const nodePayload = (body) => ({
  name: String(body.name || '').trim(), type: String(body.type || 'Concept').trim(),
  sourceType: String(body.sourceType || 'KHAI_NIEM').trim(), lesson: String(body.lesson || '').trim(),
  description: String(body.description || '').trim(), quote: String(body.quote || '').trim(),
  keyphrases: Array.isArray(body.keyphrases) ? body.keyphrases.map(String) : [],
  aliases: Array.isArray(body.aliases) ? body.aliases.map(String) : []
});
router.get('/admin/edges', ...admin, async (_req, res, next) => { try { res.json(await getEdges()); } catch (error) { next(error); } });
router.post('/admin/nodes', ...admin, async (req, res, next) => {
  try { const id = String(req.body.id || '').trim(); const node = nodePayload(req.body); if (!id || !node.name) return res.status(400).json({ error: 'id và name là bắt buộc.' }); res.status(201).json(await createNode({ id, ...node })); }
  catch (error) { if (error.message === 'NODE_EXISTS') return res.status(409).json({ error: 'Node đã tồn tại.' }); next(error); }
});
router.patch('/admin/nodes/:id', ...admin, async (req, res, next) => {
  try { const node = nodePayload(req.body); if (!node.name) return res.status(400).json({ error: 'name là bắt buộc.' }); res.json(await updateNode(req.params.id, node)); }
  catch (error) { if (error.message === 'NODE_NOT_FOUND') return res.status(404).json({ error: 'Không tìm thấy node.' }); next(error); }
});
router.delete('/admin/nodes/:id', ...admin, async (req, res, next) => {
  try { await deleteNode(req.params.id); res.status(204).end(); } catch (error) { if (error.message === 'NODE_NOT_FOUND') return res.status(404).json({ error: 'Không tìm thấy node.' }); next(error); }
});
router.patch('/admin/edges/:from/:to', ...admin, async (req, res, next) => {
  try { const weight = Number(req.body.weight); if (!Number.isFinite(weight) || weight <= 0) return res.status(400).json({ error: 'weight phải là số dương.' }); await updateEdge({ from: req.params.from, to: req.params.to, weight, reason: String(req.body.reason || '') }); res.json({ from: req.params.from, to: req.params.to, weight, reason: String(req.body.reason || '') }); }
  catch (error) { if (error.message === 'EDGE_NOT_FOUND') return res.status(404).json({ error: 'Không tìm thấy cạnh.' }); next(error); }
});
router.delete('/admin/edges/:from/:to', ...admin, async (req, res, next) => {
  try { await deleteEdge({ from: req.params.from, to: req.params.to }); res.status(204).end(); } catch (error) { if (error.message === 'EDGE_NOT_FOUND') return res.status(404).json({ error: 'Không tìm thấy cạnh.' }); next(error); }
});
router.patch('/admin/documents/:id', ...admin, async (req, res, next) => {
  try { const document = await updateDocument(req.params.id, { file: String(req.body.file || '').trim(), format: String(req.body.format || '').trim(), lesson: String(req.body.lesson || '').trim() }); res.json(document); } catch (error) { if (error.message === 'DOCUMENT_NOT_FOUND') return res.status(404).json({ error: 'Không tìm thấy tài liệu.' }); next(error); }
});
router.delete('/admin/documents/:id', ...admin, async (req, res, next) => {
  try { await deleteDocument(req.params.id); res.status(204).end(); } catch (error) { if (error.message === 'DOCUMENT_NOT_FOUND') return res.status(404).json({ error: 'Không tìm thấy tài liệu.' }); next(error); }
});

router.post('/admin/edges', requireAuth, requireRole('ADMIN'), async (req, res, next) => {
  try {
    const { from, to, reason = '' } = req.body; const weight = Number(req.body.weight ?? 1);
    if (!from || !to || !Number.isFinite(weight) || weight <= 0) return res.status(400).json({ error: 'from, to và weight dương là bắt buộc.' });
    const adjacency = await getAdjacency('forward'); if (detectCycle(from, to, adjacency)) return res.status(409).json({ error: 'Thao tác này sẽ tạo chu trình trong quan hệ TIEN_QUYET.' });
    await createEdge({ from, to, weight, reason }); res.status(201).json({ from, to, weight, reason });
  } catch (error) {
    if (error.message === 'EDGE_EXISTS_OR_ENDPOINT_MISSING') return res.status(409).json({ error: 'Cạnh đã tồn tại hoặc endpoint không hợp lệ.' });
    next(error);
  }
});

export default router;
