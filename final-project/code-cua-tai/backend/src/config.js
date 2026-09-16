import dotenv from 'dotenv';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

dotenv.config({ path: path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../.env') });

export const config = {
  port: Number(process.env.PORT || 3001),
  neo4jUri: process.env.NEO4J_URI || 'neo4j://localhost:7687',
  neo4jUser: process.env.NEO4J_USER || 'neo4j',
  neo4jPassword: process.env.NEO4J_PASSWORD || 'change-me',
  neo4jDatabase: process.env.NEO4J_DATABASE || 'neo4j',
  jwtSecret: process.env.JWT_SECRET || 'development-only-secret',
  llmBaseUrl: process.env.LLM_BASE_URL || 'http://localhost:8000/v1',
  llmApiKey: process.env.LLM_API_KEY || '',
  llmModel: process.env.LLM_MODEL || 'local-model',
  llmTimeoutMs: Number(process.env.LLM_TIMEOUT_MS || 30000)
};
