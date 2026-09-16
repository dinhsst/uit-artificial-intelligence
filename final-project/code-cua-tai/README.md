# Hệ thống tra cứu kiến thức AI

Ứng dụng tra cứu kiến thức môn Trí tuệ nhân tạo theo mô hình Knowledge Graph. Hệ thống sử dụng các thuật toán DFS, BFS, Dijkstra và A* để duyệt graph; LLM/Graph-RAG chỉ đóng vai trò hỗ trợ giải thích khi được cấu hình.

## Công nghệ

- **Backend:** Node.js, Express, Neo4j Driver, JWT, bcryptjs
- **Frontend:** React, Vite, Cytoscape.js
- **Database:** Neo4j Cloud hoặc Neo4j local
- **LLM tùy chọn:** API tương thích OpenAI, cấu hình qua biến môi trường

## Cấu trúc thư mục

```text
.
├── backend/
│   ├── src/
│   │   ├── algorithms/       # DFS, BFS, Dijkstra, A*, cycle detection
│   │   ├── db/               # Neo4j driver và schema
│   │   ├── llm/              # Graph-RAG
│   │   ├── middleware/       # JWT và phân quyền
│   │   ├── routes/           # REST API
│   │   └── services/         # Graph và authentication
│   └── tests/
├── frontend/
│   └── src/                  # React UI và API client
├── data/
│   ├── importKnowledgeBase.js
│   ├── normalized-knowledge-base.json
│   └── knowledge-base-audit.json
├── knowledge-base/           # Dữ liệu nguồn JSON/CSV
├── docker-compose.yml        # Neo4j local tùy chọn
└── package.json
```

## Yêu cầu

- Node.js 20 trở lên
- npm 10 trở lên
- Neo4j Cloud đã tạo database, hoặc Docker nếu chạy Neo4j local

## Cài đặt

```bash
npm install
```

Các workspace `backend` và `frontend` được quản lý từ `package.json` ở thư mục gốc.

## Cấu hình môi trường

Sao chép file mẫu:

```bash
cp .env.example .env
```

Trên Windows, có thể sao chép thủ công `.env.example` thành `.env`.

### Neo4j Cloud

Dùng URI bảo mật do Neo4j Cloud cung cấp, thường có dạng `neo4j+s://...`:

```env
NODE_ENV=development
PORT=3001

NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j

JWT_SECRET=replace-with-a-long-random-secret

# Tùy chọn: để trống nếu chỉ dùng fallback graph
LLM_BASE_URL=http://localhost:8000/v1
LLM_API_KEY=
LLM_MODEL=local-model
LLM_TIMEOUT_MS=30000
```

Không commit `.env`. Không dùng mật khẩu Neo4j hoặc JWT secret mẫu trong production.

Tạo JWT secret ngẫu nhiên bằng Node.js:

```bash
node -e "console.log(require('crypto').randomBytes(48).toString('hex'))"
```

## Chuẩn hóa và seed dữ liệu

### Trích xuất tài liệu từ `rawdata/`

`rawdata/` chứa PDF, DOC/DOCX và TXT thật. Công cụ Python dùng virtual environment để trích xuất text UTF-8, giữ metadata file/bài học và tạo JSONL trung gian:

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install pypdf python-docx
npm run extract:rawdata
```

Kết quả tạo tại `data/rawdata-extracted.jsonl` (đã được gitignore vì có thể lớn). Công cụ hỗ trợ PDF, DOCX, DOC legacy qua `antiword` và TXT. Hãy review audit/nội dung trước khi đưa tài liệu mới vào production.

Seed sẽ đọc JSONL này và tạo node `Document` trong Neo4j. Có thể kiểm tra qua:

```text
GET /api/documents
GET /api/documents/:id
```

Importer đọc dữ liệu kiến thức trong `knowledge-base/`, loại bỏ node trùng ID, chỉ giữ cạnh `TIEN_QUYET` được phê duyệt và ghi audit vào `data/knowledge-base-audit.json`:

```bash
npm run import
```

Seed vào Neo4j:

```bash
node backend/src/seedNeo4j.js
```

Seed hiện tạo 220 node, 156 cạnh và 17 node `Document` (khoảng 1,36 triệu ký tự) trên bộ dữ liệu hiện tại. Node tri thức được giữ label `Concept` để tương thích graph lõi, đồng thời có thêm label `Property`, `Exercise` hoặc `Method` theo loại dữ liệu. Seed có thể chạy lại để cập nhật thuộc tính, label và nội dung tài liệu.

Pipeline này đưa **toàn văn tài liệu** vào Neo4j để tra cứu/cung cấp context. Nó chưa tự động phân tích PDF/DOCX để sinh thêm node concept hoặc quan hệ `REQUIRES`; các node và quan hệ mới vẫn cần được chuẩn hóa, review và phê duyệt trước khi import.

### Neo4j local tùy chọn

Nếu không dùng Neo4j Cloud:

```bash
docker compose up -d
npm run import
node backend/src/seedNeo4j.js
```

Neo4j Browser mặc định tại `http://localhost:7474`.

## Cách sử dụng giao diện

### Trang tra cứu công khai

Mở `/` hoặc `/search` để:

- Tìm kiếm kiến thức bằng từ khóa.
- Lọc theo bài học và loại nội dung.
- Mở định nghĩa, trích dẫn, tính chất và bài tập.
- Xem tài liệu đã được nạp.
- Mở phần kiến thức liên quan khi cần.

Trang public không yêu cầu đăng nhập cho tra cứu cơ bản. Đăng nhập chỉ cần cho tiến độ cá nhân, Dijkstra/A* và Graph-RAG.

### Trang quản trị

Mở `/admin` bằng tài khoản có role `ADMIN`. Trang này dành cho:

- Xem tổng quan node, quan hệ và tài liệu.
- Kiểm tra graph và quan hệ `REQUIRES`.
- Thêm node tri thức.
- Tạo quan hệ mới sau khi backend kiểm tra endpoint, trọng số và chu trình.
- Xem danh sách tài liệu đã ingest.

User thường không được gọi API admin. Các chức năng upload tài liệu, workflow duyệt LLM và quản lý user nâng cao chưa được bật vì backend chưa có storage/workflow tương ứng.

## Chạy development

Chạy cả backend và frontend:

```bash
npm run dev
```

Hoặc chạy riêng:

```bash
npm run dev --workspace backend
npm run dev --workspace frontend
```

Địa chỉ mặc định:

- Backend API: `http://localhost:3001`
- Frontend: `http://localhost:5173`
- Health check: `http://localhost:3001/api/health`

Frontend dùng API URL mặc định `http://localhost:3001/api`. Có thể thay đổi bằng:

```env
VITE_API_URL=https://your-backend-domain.example/api
```

Chỉ đưa biến bắt đầu bằng `VITE_` vào frontend; tuyệt đối không đưa API key hoặc JWT secret vào đó.

## API chính

### Health và tra cứu

```text
GET /api/health
GET /api/concepts
GET /api/concepts/:id
GET /api/graph
GET /api/search?q=heuristic&type=Method&lesson=B2
GET /api/subjects/:subjectId/lessons
GET /api/lessons/:lessonId/concepts
```

### Nội dung theo loại

```text
GET /api/concepts/:id/properties
GET /api/concepts/:id/exercises
GET /api/exercises/:id/methods
```

### Thuật toán graph

```text
GET /api/concepts/:id/related?algorithm=bfs&max_depth=3
GET /api/concepts/:id/related?algorithm=dfs&max_depth=5
GET /api/concepts/:id/path?algorithm=dijkstra&target=<concept-id>&max_depth=100
GET /api/concepts/:id/path?algorithm=astar&target=<concept-id>&max_depth=100
```

`/path` yêu cầu header:

```text
Authorization: Bearer <jwt>
```

Dijkstra và A* chạy theo hướng lộ trình được cấu hình trong backend; A* sử dụng mastery của user để điều chỉnh chi phí cạnh.

### Tạo tài khoản quản trị viên

Đăng ký công khai luôn tạo tài khoản `USER`. Để tạo tài khoản admin lần đầu, đặt tạm thời các biến môi trường rồi chạy script bootstrap:

PowerShell:

```powershell
$env:ADMIN_NAME="Quản trị viên"
$env:ADMIN_EMAIL="admin@example.com"
$env:ADMIN_PASSWORD="mật-khẩu-tạm-thời-dài-hơn-8-ký-tự"
npm run bootstrap:admin
Remove-Item Env:ADMIN_PASSWORD
```

Git Bash:

```bash
export ADMIN_NAME="Quản trị viên"
export ADMIN_EMAIL="admin@example.com"
export ADMIN_PASSWORD="mật-khẩu-tạm-thời-dài-hơn-8-ký-tự"
npm run bootstrap:admin
unset ADMIN_PASSWORD
```

Script kết nối Neo4j theo `.env`, hash mật khẩu bằng bcrypt, tạo hoặc nâng role của đúng email thành `ADMIN`, và không in mật khẩu ra log. Sau khi chạy, xóa biến môi trường `ADMIN_PASSWORD`, đăng nhập tại `/admin`, rồi đổi hoặc thay mật khẩu theo chính sách vận hành của bạn.

## Authentication và progress

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/users/me/progress
PUT  /api/users/me/progress/:conceptId
```

Ví dụ đăng ký:

```json
{
  "name": "Người học",
  "email": "learner@example.com",
  "password": "at-least-8-characters"
}
```

### Graph-RAG

```text
POST /api/ask
Authorization: Bearer <jwt>
Content-Type: application/json
```

Body:

```json
{
  "conceptId": "B1.KN.AI",
  "question": "Khái niệm này nói về điều gì?"
}
```

Nếu chưa cấu hình LLM hoặc LLM không khả dụng, API trả fallback dựa trên graph traversal thay vì làm hỏng request.

## Kiểm thử và build

Chạy unit test backend:

```bash
npm test
```

Build frontend production:

```bash
npm run build --workspace frontend
```

Kiểm tra syntax backend:

```bash
node --check backend/src/server.js
node --check backend/src/routes/api.js
node --check backend/src/seedNeo4j.js
```

## Triển khai production

Quy trình khuyến nghị:

1. Tạo Neo4j database production riêng và backup trước migration.
2. Cấu hình secret production qua secret manager của nền tảng deploy.
3. Chạy test và build.
4. Chạy schema initialization và seed một lần trong bước deploy/migration, không chạy seed mỗi request.
5. Khởi động backend bằng:

   ```bash
   npm start --workspace backend
   ```

6. Deploy `frontend/dist` lên static hosting/CDN.
7. Đặt `VITE_API_URL` trỏ đến backend HTTPS.
8. Kiểm tra `/api/health`, đăng nhập, tìm kiếm, traversal, progress và fallback Graph-RAG.

Trước khi public rộng rãi, cần giới hạn CORS theo domain frontend, thêm rate limiting cho authentication/search/ask, validate request ở biên API và bật monitoring/backup.

## Chất lượng dữ liệu hiện tại

Kết quả normalize hiện tại:

- 220 node hợp lệ được giữ lại
- 79 cạnh `REQUIRES` Concept → Concept được đưa vào graph học tập
- 26 mapping nội dung được curated và seed thành `HAS_PROPERTY`, `APPLIED_IN`, `SOLVED_BY`, `INCLUDES`
- 23 ID trùng được audit, không âm thầm coi là các node riêng
- 607 record quan hệ bị loại/quarantine theo lý do: thiếu endpoint, endpoint không phải Concept hoặc loại quan hệ chưa được publish
- Không có node thiếu trường bắt buộc sau khi importer hỗ trợ cả `dinh_nghia` và biến thể `dinh nghia`
- Không có source type chưa biết

Quan trọng: hệ thống không còn ghép property/exercise/method chỉ vì cùng `lesson`. Nội dung chưa có mapping explicit sẽ trả trạng thái rỗng/chưa liên kết thay vì hiển thị nhầm. Mapping curated nằm tại `knowledge-base/content-mappings.json`; các quan hệ chưa đủ bằng chứng vẫn cần admin review. Xem chi tiết tại `data/knowledge-base-audit.json`. Không xóa các node độc lập chỉ vì node đó không có cạnh; chúng vẫn có giá trị cho tìm kiếm và tra cứu.

## Tài liệu đặc tả

- `he-thong-tra-cuu-kien-thuc-full-plan.md`: plan và technical specification
- `ai-knowledge-graph.md`: sơ đồ ontology và quan hệ tri thức
