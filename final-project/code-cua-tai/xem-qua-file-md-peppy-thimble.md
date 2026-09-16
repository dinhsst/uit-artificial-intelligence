# Context

Tài liệu [he-thong-tra-cuu-kien-thuc-full-plan.md](c:\Users\Boss\Desktop\nhom26 git\uit-artificial-intelligence\final-project\code-cua-tai\he-thong-tra-cuu-kien-thuc-full-plan.md) mô tả một hệ thống tra cứu kiến thức môn Trí tuệ nhân tạo theo mô hình Hybrid Symbolic-Neural. Hiện thư mục `code-cua-tai` chỉ có tài liệu đặc tả; các nguồn dữ liệu dùng được nằm ở `final-project/knowledge-base/`, chưa có mã nguồn, `package.json` hay schema/seed Neo4j.

Mục tiêu nên là dựng một MVP chạy được và kiểm chứng được trước; các phần LLM, analytics, versioning, accessibility nâng cao, observability và CI/CD để sau MVP. Lõi bắt buộc là các thuật toán graph tự triển khai, không giao việc tìm kiếm cho LLM.

# Phạm vi đề xuất

## MVP 1 — nền tảng và dữ liệu

- Khởi tạo monorepo gồm `backend/`, `frontend/`, `data/`, `docs/` và cấu hình chạy local.
- Chạy Neo4j bằng Docker Compose và xây pipeline import/chuẩn hóa từ `final-project/knowledge-base/`: import mọi node hợp lệ trong `nodes_tho.json`; dùng `relations.json` cho cạnh `TIEN_QUYET`, nhưng chỉ nạp cạnh có cặp nguồn/đích khớp `phieu_duyet_tien_quyet.csv` với `DUYỆT=true`; dùng `corpus.json` làm nguồn text phục vụ tìm kiếm/Graph-RAG.
- Trước khi import, validate referential integrity (mọi endpoint của cạnh phải tồn tại), ID trùng, bản ghi thiếu trường và mapping `loai` → loại node trong schema. Node độc lập vẫn được giữ để tìm kiếm/tra cứu; cạnh lỗi, chưa duyệt hoặc trỏ tới node thiếu được bỏ qua và xuất báo cáo audit. Không import mù vì hiện đã thấy quan hệ trỏ tới một số ID chưa chắc có trong danh sách node và có ID node bị lặp.
- Tích hợp LLM qua một OpenAI-compatible adapter: `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` và timeout/rate-limit cấu hình bằng env; không hard-code provider hoặc URL. Graph-RAG nhận subgraph do traversal tạo ra, có cache/fallback và không gửi thông tin định danh người học.
- Dữ liệu tiếng Việt được giữ nguyên UTF-8; corpus được map theo ID nguồn để làm context cho câu trả lời.

## MVP 2 — lõi graph và kiểm thử

- Cài đặt contract traversal thống nhất: DFS, BFS, Dijkstra, A* và cycle detection.
- Bổ sung kiểm tra input ở biên API: thuật toán hợp lệ, `max_depth` hữu hạn, node/target tồn tại, trọng số không âm.
- Quy định rõ thứ tự neighbor để DFS/BFS cho kết quả deterministic; dùng priority queue cho Dijkstra/A*.
- Viết unit test độc lập cho graph rỗng, node không tồn tại, graph rời rạc, chu trình, graph sâu, target không reachable và các đường đi có trọng số.
- Đặc biệt rà soát hướng cạnh `REQUIRES`: nếu A `REQUIRES` B nghĩa là A cần học B trước, endpoint “lộ trình đến mục tiêu” phải duyệt ngược cạnh hoặc seed thêm quan hệ định hướng phù hợp; không được để UI diễn giải ngược ý nghĩa.

## MVP 3 — API và xác thực

- Tạo các endpoint lesson → concept, concept → property/exercise, exercise → method, search và related/path theo đúng API contract trong mục 27.
- Thêm middleware JWT và bcrypt, hai vai trò Admin/User; bảo vệ toàn bộ `/api/admin/*` bằng role check.
- Endpoint tạo cạnh `REQUIRES` phải chạy cycle detection trong cùng luồng kiểm tra trước khi ghi.
- Trả lỗi nhất quán cho không tìm thấy dữ liệu, path không tồn tại, query sai và lỗi Neo4j; không để lỗi driver lộ ra response.
- Lưu progress tối thiểu theo user/concept và chỉ cho người dùng cập nhật progress của chính họ; A* lấy mastery từ phiên đăng nhập, dùng giá trị 0 nếu chưa có bản ghi.

## MVP 4 — giao diện và kiểm thử tích hợp

- Dựng React layout ba vùng theo wireframe: sidebar Subject/Lesson/Concept, detail panel và Cytoscape graph.
- Thêm tìm kiếm cơ bản, tab properties/exercises/methods, lựa chọn DFS/BFS/Dijkstra/A*, `max_depth`, target và hiển thị `visited_order`/path/cost.
- Hiển thị trạng thái loading, empty, không có path và lỗi; graph visualization chỉ là lớp trình bày, không chứa logic traversal riêng.
- Viết integration test API với Neo4j test database/container và kiểm tra golden path từ dữ liệu seed; kiểm thử UI tối thiểu bằng cách chạy frontend/backend thực tế.

## Phạm vi đã chốt cho MVP

- Lõi tra cứu graph và 4 thuật toán; giữ cạnh dữ liệu theo hướng `A → B` nhưng truy vấn ngược khi xây lộ trình đến A.
- Auth Admin/User bằng JWT/bcrypt.
- Lưu tiến độ học tối thiểu theo user/concept với `mastery` trong khoảng 0–1; A* điều chỉnh chi phí cạnh theo `cost × (1 − mastery)` (đặt floor dương nhỏ để tránh đường đi 0), còn heuristic là khoảng cách ước lượng đến mục tiêu.
- Tích hợp LLM Graph-RAG có cấu hình API key, nhưng traversal vẫn là nguồn dữ liệu bắt buộc và có fallback khi LLM lỗi.
- Docker Compose cho Neo4j.

## Sau MVP

- Offline LLM extraction có human approval; quiz tự sinh.
- Progress/mastery nâng cao và đánh giá heuristic A*.
- Fuzzy search, analytics, versioning/coverage check, backup/export, accessibility nâng cao, cost control, observability, CI/CD và multi-subject template.

# Tệp dự kiến tạo/sửa

- Root: `README.md`, `.env.example`, `docker-compose.yml`, `package.json` và workspace configuration.
- Dữ liệu: `data/importKnowledgeBase.*` (validate/dedupe/import/audit), `data/seed_ai_subject.cypher` hoặc seed runner, cùng test fixture nhỏ tách từ `final-project/knowledge-base/`.
- Backend: `backend/src/db/`, `algorithms/`, `services/`, `routes/`, `middleware/`, `models/`, `llm/`, `backend/tests/`.
- Frontend: `frontend/src/components/`, `pages/`, `api/`, `App.*`.

# Quyết định đã chốt

- Neo4j chạy local bằng Docker Compose.
- Import mọi node hợp lệ từ `final-project/knowledge-base/nodes_tho.json`; node độc lập vẫn tìm kiếm/tra cứu được.
- Cạnh chỉ được import nếu tồn tại trong `relations.json`, hai endpoint tồn tại sau normalize, và cặp nguồn/đích khớp `phieu_duyet_tien_quyet.csv` có `DUYỆT=true`; phần bị loại xuất thành audit report.
- Giữ dữ liệu `TIEN_QUYET` theo hướng concept cần học → concept tiên quyết. Các API lộ trình học đi ngược chiều cạnh để từ prerequisite dẫn đến mục tiêu; API liệt kê điều kiện tiên quyết đi theo chiều dữ liệu.
- Auth JWT/bcrypt có hai vai trò Admin/User; MVP lưu mastery theo user/concept.
- A* dùng effective cost `max(epsilon, base_cost × (1 − mastery_of_next_concept))`; `mastery` mặc định 0. Heuristic phải là ước lượng lower-bound khoảng cách còn lại và được test để không làm mất tính tối ưu.
- Graph-RAG dùng adapter tương thích OpenAI `/v1`, cấu hình bằng `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`; graph traversal tạo context có cấu trúc, và endpoint trả fallback traversal nếu LLM timeout/rate-limit/lỗi.

# Kiểm chứng

1. Chạy import vào Neo4j mới, kiểm tra constraints/index, số node, số cạnh được nhận/bỏ và audit report; xác nhận không còn cạnh mồ côi/ID trùng.
2. Unit test DFS/BFS/Dijkstra/A*/cycle detection với graph rỗng, disconnected, cycle, sâu, nhiều đường có trọng số và mastery 0/1.
3. Integration test: API lesson/concept/search/related/path, cycle bị từ chối, non-existent path, phân quyền, cập nhật progress của chính user và Graph-RAG fallback.
4. Khởi động full stack qua Docker Compose, dùng UI thực hiện luồng đăng nhập → chọn bài/concept → tìm tiền quyết/lộ trình → cập nhật mastery → so sánh Dijkstra và A* → hỏi Graph-RAG; xác nhận graph highlight, trạng thái loading/empty/error và tiếng Việt hiển thị đúng UTF-8.

# Điểm cần theo dõi khi thực hiện

- `nodes_tho.json`, `relations.json` và các CSV không hoàn toàn đồng nhất; importer cần là nguồn chuẩn hóa duy nhất, không sửa dữ liệu gốc trong MVP.
- Mapping các loại `KHAI_NIEM`, `TINH_CHAT`, `PP_GIAI`, `BT`, `VI_DU`, `NGUYEN_LY`, ... sang labels/schema UI phải được làm data-driven để không loại dữ liệu ngoài sáu loại node trong spec cũ.
- Chỉ dùng dữ liệu tri thức/subgraph/corpus trong prompt LLM; tuyệt đối không đưa email, password, JWT hoặc hồ sơ định danh của user vào prompt/log.
