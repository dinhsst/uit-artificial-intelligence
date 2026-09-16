import neo4j from 'neo4j-driver';
import { config } from '../config.js';

export const driver = neo4j.driver(
  config.neo4jUri,
  neo4j.auth.basic(config.neo4jUser, config.neo4jPassword),
  { disableLosslessIntegers: true }
);

export async function runQuery(query, params = {}) {
  const session = driver.session({ database: config.neo4jDatabase });
  try {
    const result = await session.run(query, params);
    return result.records;
  } finally {
    await session.close();
  }
}

export function recordToObject(record) {
  return record.toObject();
}
