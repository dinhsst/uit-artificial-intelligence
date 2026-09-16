import { driver, runQuery } from './neo4j.js';
import { schemaStatements } from './schema.js';

export async function initializeSchema() {
  for (const statement of schemaStatements) await runQuery(statement);
}

export async function closeDatabase() { await driver.close(); }
