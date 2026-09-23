# CPP Atlas

CPP Atlas là vertical slice của nền tảng học C++ theo hướng **Knowledge + Practice + Visualization**. Ứng dụng hiện chạy frontend-first, với content và graph relation nằm trong data layer để sẵn sàng chuyển sang Next.js/FastAPI/PostgreSQL ở các milestone tiếp theo.

## Đã có trong MVP

- Content pack canonical song ngữ: 52 lesson bài giảng chi tiết cho người mới, 39 knowledge items, 13 exercises, 20 quizzes và 11 visualizations.
- Trang chủ và learning path 13 chương, mỗi chapter mở đúng lesson đầu tiên trong content.
- Catalog bài tập và visualization có filter/entry point riêng.
- Search có debounce, filter theo loại/chương, suggestions và API/local fallback.
- Topic page có graph zoom/reset, relation list, recommendation reason, examples, problem types và common mistakes.
- Quiz có retry, review explanation và link ôn lại knowledge.
- Playground có starter code, stdin, gọi runner API khi sẵn sàng và trạng thái offline trung thực.
- FastAPI REST API `/api/v1` với knowledge, search, graph, exercise, auth, progress, code-run proxy, AI fallback và admin overview.
- PostgreSQL schema/migration bằng Alembic, seed data, Redis service và Compose service boundaries.
- Runner C++17 riêng với source-policy checks, compile/runtime states, timeout/resource limits, non-root container và network nội bộ kín.
- Search tiếng Việt có dấu/không dấu, từ khóa tự nhiên và typo nhẹ.
- Knowledge topic: definition, properties, syntax, prerequisites, next/related knowledge.
- Knowledge graph neighborhood giới hạn bằng BFS và recommendation có lý do.
- Exercise flow: strategy, pseudocode, 3 hint, solution, required knowledge.
- Visualization step-by-step cho trace bài học được định nghĩa sẵn.
- Playground C++17-style editor với trạng thái demo an toàn.
- Quiz và progress lưu ở `localStorage`.
- Responsive layout, focus-friendly controls và textual fallback cho graph/visualization.
- Docker image static Nginx, SPA fallback và `/healthz`.

## Chạy local

Yêu cầu Node.js 20+.

```bash
npm install
npm run dev
```

Mở `http://localhost:4173`.

Kiểm tra production build:

```bash
npm run test
npm run build
npm run preview
```

## Chạy bằng Docker

Copy `.env.example` thành `.env`, đổi `JWT_SECRET` thành chuỗi ngẫu nhiên dài, sau đó:

```bash
docker compose up --build -d
```

Các cổng mặc định được chọn để tránh xung đột môi trường dùng chung:

- Web: `http://localhost:8080`
- API: `http://localhost:18000/docs`
- PostgreSQL: `localhost:55433`
- Redis: `localhost:56379`

Mở `http://localhost:8080`. API container tự chạy `alembic upgrade head` và seed trước khi serve. Với môi trường bị giới hạn Docker Hub, cần preload các base images (`node:20-alpine`, `python:3.12-slim`, `postgres:16`, `redis:7-alpine`) trước khi chạy.

Smoke checks:

```bash
curl http://localhost:18000/healthz
curl 'http://localhost:18000/api/v1/search?q=tim%20max%20mang'
```

Không dùng `docker compose down -v` trên database production vì lệnh đó xóa volumes.

## Luồng demo chính

1. Homepage → `Bắt đầu tra cứu`.
2. Tìm `tìm số lớn nhất trong mảng` hoặc `tim max mang`.
3. Mở topic `Tìm số lớn nhất trong mảng`.
4. Chọn `Vòng lặp`/`Mảng` trong graph hoặc danh sách liên quan.
5. Mở bài tập → strategy → hint → solution.
6. Mở visualization và step qua trace.
7. Làm quiz → xem progress.

## Cấu trúc

- `content/`: source data syllabus; content demo domain hiện được validate và export trong `src/domain/content.ts`.
- `src/domain/`: types, search, graph/recommendation, progress.
- `src/App.tsx`: routing hash và page composition của vertical slice.
- `src/styles.css`: visual system responsive.
- `tests/`: search, graph/recommendation và content contract.
- `deploy/`: Nginx SPA config.

## Security và giới hạn production

Playground browser chưa tự gọi arbitrary code; endpoint thật nằm ở API và proxy tới runner riêng. Runner dùng C++17, kiểm tra source, timeout, `setrlimit`, non-root container, read-only rootfs, tmpfs workspace, dropped capabilities, `no-new-privileges` và network nội bộ không có egress. Trace cho code tự do vẫn trả `trace_available=false`; không tạo trace giả. Trước public deployment cần bổ sung seccomp profile, image scanning, resource quotas ở orchestration layer, authenticated runner channel/mTLS và workflow Submit với hidden tests.

Auth API dùng username/password, Argon2id, JWT bearer hiện tại; public deployment nên đặt HttpOnly Secure SameSite session cookie sau reverse proxy TLS, rotate secret và thêm persistent login rate-limit/shared store. Progress API lọc theo `current_user`, chống IDOR cho learner. Admin overview yêu cầu role `ADMIN`; không có endpoint tự nâng quyền.

AI abstraction chỉ đọc key ở backend environment. Khi chưa đủ `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`, `/api/v1/ai/ask` trả fallback minh bạch và Knowledge Base không bị phụ thuộc AI. Không đặt key trong Vite env/frontend.

## Roadmap production còn lại

- Kết nối frontend qua API client có auth/session thay cho local content/progress; giữ local fallback khi API offline.
- M2–M4: PostgreSQL FTS/pg_trgm/pgvector lexical fallback, graph settings/metrics và recommendation backend ranking.
- M5–M7: exercise public/hidden judging, authenticated runner channel và realtime trace instrumentation.
- M8–M10: đầy đủ AI modes/schema validation/citations, CMS CRUD/audit/snapshot restore, backup, accessibility/performance/security/e2e CI.

## Kiểm thử

```bash
npm run test && npm run build
pytest -q api/tests
pytest -q runner/test_runner.py
python3 -m compileall -q api runner
```

Các test backend dùng SQLite chỉ để cô lập logic; acceptance production phải chạy thêm với PostgreSQL container và Docker image scanner.
