import express from 'express';
import cors from 'cors';
import api from './routes/api.js';
import { config } from './config.js';
import { initializeSchema } from './db/initialize.js';

const app = express();
app.use(cors());
app.use(express.json({ limit: '1mb' }));
app.use('/api', api);
app.use((error, _req, res, _next) => { console.error(error); res.status(500).json({ error: 'Đã xảy ra lỗi máy chủ.' }); });

if (process.env.NODE_ENV !== 'test') {
  initializeSchema().then(() => app.listen(config.port, () => console.log(`Backend listening on ${config.port}`))).catch((error) => { console.error('Database initialization failed', error); process.exitCode = 1; });
}
export default app;
