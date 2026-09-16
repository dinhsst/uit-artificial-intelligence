import { randomUUID } from 'node:crypto';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { config } from '../config.js';
import { runQuery } from '../db/neo4j.js';

export async function register({ name, email, password }) {
  const existing = await runQuery('MATCH (u:User {email:$email}) RETURN u LIMIT 1', { email });
  if (existing.length) throw new Error('EMAIL_EXISTS');
  const id = randomUUID();
  const role = 'USER';
  const passwordHash = await bcrypt.hash(password, 12);
  await runQuery('CREATE (u:User {id:$id, name:$name, email:$email, passwordHash:$passwordHash, role:$role})', { id, name, email, passwordHash, role });
  return { id, name, email, role };
}

export async function authenticate({ email, password }) {
  const records = await runQuery('MATCH (u:User {email:$email}) RETURN u LIMIT 1', { email });
  const user = records[0]?.get('u').properties;
  if (!user || !(await bcrypt.compare(password, user.passwordHash))) return null;
  return { id: user.id, name: user.name, email: user.email, role: user.role };
}

export function issueToken(user) {
  return jwt.sign({ sub: user.id, role: user.role, name: user.name }, config.jwtSecret, { expiresIn: '8h' });
}

export async function updateMastery(userId, conceptId, mastery) {
  await runQuery(`MATCH (u:User {id:$userId}), (c:Concept {id:$conceptId})
    MERGE (p:Progress {user_id:$userId, concept_id:$conceptId})
    SET p.mastery=$mastery, p.updatedAt=datetime()
    MERGE (u)-[:HAS_PROGRESS]->(p)
    MERGE (p)-[:FOR_CONCEPT]->(c)`, { userId, conceptId, mastery });
  return { conceptId, mastery };
}

export async function getMastery(userId) {
  const records = await runQuery('MATCH (p:Progress {user_id:$userId}) RETURN p.concept_id AS conceptId, p.mastery AS mastery', { userId });
  return new Map(records.map((record) => [record.get('conceptId'), Number(record.get('mastery'))]));
}
