import { afterEach, describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { aStar, bfsTraverse, buildAdjacency, detectCycle, dfsTraverse, dijkstra } from '../src/algorithms/traversal.js';

const edges = [
  { from: 'A', to: 'B', weight: 2 },
  { from: 'A', to: 'C', weight: 1 },
  { from: 'B', to: 'D', weight: 1 },
  { from: 'C', to: 'D', weight: 5 },
  { from: 'D', to: 'E', weight: 1 }
];
const forward = buildAdjacency(edges);

describe('graph traversal', () => {
  it('uses deterministic DFS and honors max depth', () => {
    const result = dfsTraverse('A', forward, 1);
    assert.deepEqual(result.visited_order.map(({ id }) => id), ['A', 'B', 'C']);
    assert.equal(result.depth_reached, 1);
  });
  it('visits by breadth and terminates on cycles', () => {
    const cycle = buildAdjacency([...edges, { from: 'E', to: 'A', weight: 1 }]);
    const result = bfsTraverse('A', cycle, 10);
    assert.deepEqual(result.visited_order.map(({ id }) => id), ['A', 'B', 'C', 'D', 'E']);
  });
  it('finds the lowest-cost weighted path', () => {
    const result = dijkstra('A', 'D', forward);
    assert.deepEqual(result.path, ['A', 'B', 'D']);
    assert.equal(result.total_cost, 3);
  });
  it('returns an empty path when disconnected', () => {
    const result = dijkstra('A', 'Z', forward);
    assert.deepEqual(result.path, []);
    assert.equal(result.total_cost, Infinity);
  });
  it('reduces A-star costs using next-concept mastery', () => {
    const mastery = new Map([['B', 1], ['D', 0]]);
    const result = aStar('A', 'D', forward, mastery);
    assert.deepEqual(result.path, ['A', 'B', 'D']);
    assert.equal(result.total_cost, 1.001);
  });
  it('detects whether a proposed prerequisite produces a cycle', () => {
    assert.equal(detectCycle('D', 'A', forward), true);
    assert.equal(detectCycle('A', 'E', forward), false);
  });
});
