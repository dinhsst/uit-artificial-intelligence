export function sortNeighbors(neighbors) {
  return [...neighbors].sort((a, b) => String(a.id).localeCompare(String(b.id)));
}

export function buildAdjacency(edges, direction = 'forward') {
  const adjacency = new Map();
  for (const edge of edges) {
    const from = direction === 'forward' ? edge.from : edge.to;
    const to = direction === 'forward' ? edge.to : edge.from;
    if (!adjacency.has(from)) adjacency.set(from, []);
    adjacency.get(from).push({ id: to, weight: edge.weight ?? 1 });
  }
  for (const [id, neighbors] of adjacency) adjacency.set(id, sortNeighbors(neighbors));
  return adjacency;
}

export function dfsTraverse(start, adjacency, maxDepth = 5) {
  const visited = new Set(); const order = []; let depthReached = 0; let cycleDetected = false;
  function visit(id, depth, stack) {
    if (depth > maxDepth) return;
    depthReached = Math.max(depthReached, depth);
    if (stack.has(id)) { cycleDetected = true; return; }
    if (visited.has(id)) return;
    visited.add(id); order.push({ id, depth }); stack.add(id);
    for (const neighbor of adjacency.get(id) || []) visit(neighbor.id, depth + 1, stack);
    stack.delete(id);
  }
  visit(start, 0, new Set());
  return { visited_order: order, depth_reached: depthReached, cycle_detected: cycleDetected };
}

export function bfsTraverse(start, adjacency, maxDepth = 5) {
  const visited = new Set([start]); const queue = [[start, 0]]; const order = []; let depthReached = 0;
  for (let index = 0; index < queue.length; index += 1) {
    const [id, depth] = queue[index];
    if (depth > maxDepth) continue;
    depthReached = Math.max(depthReached, depth); order.push({ id, depth });
    for (const neighbor of adjacency.get(id) || []) if (!visited.has(neighbor.id)) { visited.add(neighbor.id); queue.push([neighbor.id, depth + 1]); }
  }
  return { visited_order: order, depth_reached: depthReached, cycle_detected: hasReachableCycle(start, adjacency, maxDepth) };
}

function hasReachableCycle(start, adjacency, maxDepth = Infinity) {
  const visiting = new Set(); const visited = new Set();
  function visit(id, depth) {
    if (depth > maxDepth) return false;
    if (visiting.has(id)) return true;
    if (visited.has(id)) return false;
    visiting.add(id);
    for (const neighbor of adjacency.get(id) || []) if (visit(neighbor.id, depth + 1)) return true;
    visiting.delete(id); visited.add(id); return false;
  }
  return visit(start, 0);
}

function pathResult(start, target, previous, distance, visitedOrder, cycleDetected = false) {
  const targetDistance = distance.get(target);
  if (!Number.isFinite(targetDistance)) return { visited_order: visitedOrder, path: [], total_cost: Infinity, depth_reached: 0, cycle_detected: cycleDetected };
  const path = []; let current = target;
  while (current !== undefined) { path.unshift(current); if (current === start) break; current = previous.get(current); }
  return { visited_order: visitedOrder, path, total_cost: targetDistance, depth_reached: path.length - 1, cycle_detected: cycleDetected };
}

export function dijkstra(start, target, adjacency, maxDepth = Infinity, cost = (edge) => edge.weight ?? 1) {
  const distance = new Map([[start, 0]]); const previous = new Map(); const queue = [{ id: start, priority: 0, depth: 0 }]; const visited = new Set(); const visitedOrder = [];
  while (queue.length) {
    queue.sort((a, b) => a.priority - b.priority || a.id.localeCompare(b.id));
    const current = queue.shift(); if (visited.has(current.id)) continue; visited.add(current.id); visitedOrder.push(current.id);
    if (current.id === target) break;
    if (current.depth >= maxDepth) continue;
    for (const edge of adjacency.get(current.id) || []) {
      const nextDistance = current.priority + cost(edge);
      if (nextDistance < (distance.get(edge.id) ?? Infinity)) { distance.set(edge.id, nextDistance); previous.set(edge.id, current.id); queue.push({ id: edge.id, priority: nextDistance, depth: current.depth + 1 }); }
    }
  }
  return pathResult(start, target, previous, distance, visitedOrder, hasReachableCycle(start, adjacency, maxDepth));
}

export function aStar(start, target, adjacency, mastery = new Map(), maxDepth = Infinity, heuristic = () => 0) {
  const effectiveCost = (edge) => Math.max(0.001, (edge.weight ?? 1) * (1 - Math.min(1, Math.max(0, mastery.get(edge.id) ?? 0))));
  const g = new Map([[start, 0]]); const previous = new Map(); const queue = [{ id: start, f: heuristic(start), g: 0, depth: 0 }]; const visited = new Set(); const visitedOrder = [];
  while (queue.length) {
    queue.sort((a, b) => a.f - b.f || a.id.localeCompare(b.id));
    const current = queue.shift(); if (visited.has(current.id)) continue; visited.add(current.id); visitedOrder.push(current.id);
    if (current.id === target) break;
    if (current.depth >= maxDepth) continue;
    for (const edge of adjacency.get(current.id) || []) {
      const nextG = current.g + effectiveCost(edge);
      if (nextG < (g.get(edge.id) ?? Infinity)) { g.set(edge.id, nextG); previous.set(edge.id, current.id); queue.push({ id: edge.id, g: nextG, f: nextG + heuristic(edge.id), depth: current.depth + 1 }); }
    }
  }
  return pathResult(start, target, previous, g, visitedOrder, hasReachableCycle(start, adjacency, maxDepth));
}

export function detectCycle(from, to, adjacency) {
  const visited = new Set(); const stack = [to];
  while (stack.length) { const id = stack.pop(); if (id === from) return true; if (visited.has(id)) continue; visited.add(id); for (const edge of adjacency.get(id) || []) stack.push(edge.id); }
  return false;
}
