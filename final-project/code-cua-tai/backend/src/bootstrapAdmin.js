import bcrypt from 'bcryptjs';
import { randomUUID } from 'node:crypto';
import { closeDatabase, initializeSchema } from './db/initialize.js';
import { driver, runQuery } from './db/neo4j.js';

const email = String(process.env.ADMIN_EMAIL || '').trim().toLowerCase();
const password = String(process.env.ADMIN_PASSWORD || '');
const name = String(process.env.ADMIN_NAME || 'Administrator').trim();

if (!email || !password || password.length < 8) {
  throw new Error('ADMIN_EMAIL và ADMIN_PASSWORD (tối thiểu 8 ký tự) là bắt buộc.');
}

try {
  await initializeSchema();
  const existing = await runQuery('MATCH (u:User {email:$email}) RETURN u LIMIT 1', { email });
  if (existing.length) {
    await runQuery('MATCH (u:User {email:$email}) SET u.role=\'ADMIN\', u.name=$name RETURN u', { email, name });
    console.log(`Admin account updated: ${email}`);
  } else {
    const passwordHash = await bcrypt.hash(password, 12);
    await runQuery(`CREATE (u:User {id:$id, name:$name, email:$email, passwordHash:$passwordHash, role:'ADMIN'})`, {
      id: randomUUID(), name, email, passwordHash
    });
    console.log(`Admin account created: ${email}`);
  }
} finally {
  await driver.close();
}
