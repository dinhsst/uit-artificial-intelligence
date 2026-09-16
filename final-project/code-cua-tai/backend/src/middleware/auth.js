import jwt from 'jsonwebtoken';
import { config } from '../config.js';

export function requireAuth(req, res, next) {
  const token = req.get('authorization')?.replace(/^Bearer\s+/i, '');
  if (!token) return res.status(401).json({ error: 'Cần đăng nhập.' });
  try { req.user = jwt.verify(token, config.jwtSecret); return next(); }
  catch { return res.status(401).json({ error: 'Phiên đăng nhập không hợp lệ hoặc đã hết hạn.' }); }
}

export function requireRole(role) {
  return (req, res, next) => req.user?.role === role ? next() : res.status(403).json({ error: 'Bạn không có quyền thực hiện thao tác này.' });
}
