# HỆ THỐNG TRA CỨU KIẾN THỨC MÔN HỌC LẬP TRÌNH
### Plan chính thức + Spec kỹ thuật thi hành được (gộp 1 file)

> Tài liệu này dùng để giao cho AI agent / lập trình viên triển khai phần mềm.
> Môn học minh họa: **Trí tuệ nhân tạo (AI)** — có thể tái sử dụng cho các môn khác (Nhập môn lập trình, Cấu trúc dữ liệu, OOP...).
> Phần I là **plan/requirements** (làm gì và tại sao). Phần II là **spec kỹ thuật** (làm như thế nào, bằng công nghệ gì, code ra sao).

---
---

# PHẦN I — PLAN TỔNG THỂ

## 1. Mục tiêu hệ thống

Xây dựng hệ thống tra cứu kiến thức cho một môn học lập trình, đáp ứng các chức năng cốt lõi:

- Tra cứu theo nội dung bài học.
- Tra cứu theo phân loại kiến thức: Khái niệm, Tính chất, Dạng bài tập + phương pháp giải.
- Tra cứu theo kiến thức liên quan (dựa trên quan hệ tiên quyết giữa các khái niệm).

**Nguyên tắc thiết kế cốt lõi:** cơ chế tìm kiếm/truy vấn tri thức **ưu tiên dùng các thuật toán duyệt graph kinh điển (DFS, BFS, Dijkstra, A\*)** làm lõi xử lý — đảm bảo tính chính xác, có thể giải thích được từng bước. **LLM chỉ hỗ trợ các phần còn lại**: xây dựng/enrich dữ liệu, sinh nội dung học tập, giải thích, hỏi-đáp tự nhiên. Đây là mô hình **Hybrid Symbolic-Neural Knowledge System**.

---

## 2. Mô hình dữ liệu (Data Model / Ontology)

### 2.1. Các loại Node

| Node | Thuộc tính chính | Ví dụ |
|---|---|---|
| Subject | id, name, description | "Trí tuệ nhân tạo" |
| Lesson | id, title, file_ref, order | "Phương pháp tìm kiếm" (3. Phuong phap tim kiem.pdf) |
| Concept | id, name, description, difficulty_level | "Thuật giải A*" |
| Property | id, statement, latex_formula | "f(n) = g(n) + h(n)" |
| Exercise | id, description, input_file, difficulty | "DothiAStart.txt" |
| Method | id, code_file, language, complexity_note | "AStart.docx" |

### 2.2. Các loại Edge (quan hệ)

| Edge | Ý nghĩa | Ví dụ |
|---|---|---|
| HAS_LESSON | Subject chứa Lesson | AI → Phương pháp tìm kiếm |
| INCLUDES | Lesson chứa Concept | Lesson → A* |
| HAS_PROPERTY | Concept có Tính chất | A* → f(n)=g(n)+h(n) |
| APPLIED_IN | Concept áp dụng vào Bài tập | A* → DothiAStart.txt |
| SOLVED_BY | Exercise được giải bằng Method | Bài tập → AStart.docx |
| **REQUIRES** | Concept này **yêu cầu** Concept khác (tiên quyết) — **trục chính cho "kiến thức liên quan"** | A* → Heuristic, A* → Dijkstra, Minimax → DFS |

**Ghi chú kỹ thuật:**
- Cạnh `REQUIRES` cần có **trọng số (weight)** để phục vụ Dijkstra tính lộ trình học ngắn nhất/nhẹ nhất.
- Cần cơ chế **cycle detection** trên `REQUIRES` để tránh vòng lặp vô hạn khi duyệt (A yêu cầu B, B lại yêu cầu A do nhập liệu sai).

---

## 3. Chức năng tra cứu (bám đúng yêu cầu đề bài)

- Tra cứu theo nội dung bài học (duyệt theo Lesson).
- Tra cứu theo phân loại: Khái niệm / Tính chất / Dạng bài tập + phương pháp giải.
- Tra cứu theo kiến thức liên quan (duyệt cạnh `REQUIRES`).
- Tìm kiếm từ khóa tự do (full-text search trên name/description).
- Bộ lọc kết hợp AND/OR (theo Subject + loại Node + độ khó).
- Gợi ý tự động (autocomplete) + fuzzy matching (Levenshtein/trigram) để xử lý lỗi gõ chính tả.
- Kết quả có xếp hạng liên quan (ranking theo độ khớp tên, số lượng liên kết, mức độ phổ biến).

---

## 4. Cơ chế thuật toán duyệt Graph (LÕI KỸ THUẬT — không dùng LLM)

Đây là phần **bắt buộc tự triển khai bằng thuật toán**, không giao cho LLM xử lý:

- **DFS (Depth-First Search):** liệt kê toàn bộ kiến thức tiên quyết theo nhánh sâu (VD: A* → Heuristic, Dijkstra → DFS nếu có liên kết chéo).
- **BFS (Breadth-First Search):** liệt kê kiến thức liên quan theo từng lớp gần-xa, phù hợp hiển thị "mức độ liên quan".
- **Dijkstra:** tìm lộ trình học "nhẹ nhất" từ kiến thức đã biết đến kiến thức mục tiêu (dựa trên trọng số cạnh `REQUIRES`).
- **A\*:** gợi ý lộ trình học cá nhân hóa, dùng heuristic ước lượng dựa trên tiến độ học của từng người dùng (mastery level).
- Setting cho phép người dùng **chọn thuật toán duyệt** để so sánh trực quan kết quả (mục đích minh họa + học thuật).
- Giới hạn độ sâu truy vấn (**max-depth**) có thể cấu hình trong settings, tránh trả kết quả quá rộng trên graph lớn.
- Cần **unit test** riêng cho từng thuật toán: graph có chu trình, graph rời rạc, graph rất sâu, graph rỗng.

---

## 5. Vai trò của LLM (hỗ trợ, KHÔNG thay thế thuật toán tìm kiếm)

### 5.1. Xây dựng & làm giàu Knowledge Graph (offline pipeline)

- Trích xuất Node/Edge tự động từ file gốc (PDF/DOCX) — LLM đọc tài liệu, đề xuất Concept/Property/Method và quan hệ `REQUIRES` giữa các Concept.
- Cần cơ chế **human-in-the-loop**: LLM chỉ đề xuất, người quản trị duyệt trước khi ghi vào graph — tránh sai sót vì đây là trục chính cho tính năng "kiến thức liên quan".
- Parse tài liệu theo cấu trúc cây (chương → bài → đoạn) trước, LLM enrich nội dung sau — giữ đúng cấu trúc gốc, tránh LLM tự suy diễn sai.

### 5.2. Hỏi-đáp tự nhiên (Graph-RAG, online pipeline)

- Người dùng hỏi câu tự nhiên (VD: "Học A* cần biết gì trước?") → hệ thống chạy DFS/Dijkstra lấy subgraph liên quan → đưa subgraph vào prompt cho LLM sinh câu trả lời diễn giải.
- Multi-hop reasoning: trả lời câu hỏi cần đi qua nhiều node liên tiếp trong graph.
- Kết hợp thêm vector/embedding search cho phần mô tả tự do, không chỉ dựa vào graph traversal thuần.

### 5.3. Sinh nội dung học tập

- Sinh câu hỏi trắc nghiệm (MCQ) từ Concept + Property + Exercise liên quan, kèm ước lượng độ khó dựa trên độ sâu/số lượng quan hệ trong graph (interpretable difficulty).
- Sinh bài tập cá nhân hóa theo mastery level của từng người dùng.
- Diễn giải lời giải (Method/code) theo văn phong sư phạm, giải thích từng bước.

### 5.4. Kiến trúc kỹ thuật khi tích hợp LLM

- Tách 2 pipeline riêng: **offline** (LLM xây/enrich graph — chạy khi có tài liệu mới) và **online** (LLM trả lời real-time dựa trên graph có sẵn).
- Cache câu trả lời LLM theo hash của subgraph truy xuất để giảm chi phí gọi API.
- Công cụ tham khảo: Neo4j LLM Knowledge Graph Builder (no-code demo nhanh) hoặc LlamaIndex `KnowledgeGraphIndex` (tự code pipeline Python).

---

## 6. Giao diện (UI/UX)

- Sidebar dạng cây (tree-structure) theo Subject → Lesson → Concept.
- Panel chi tiết node: hiển thị Property, Exercise, Method liên quan.
- Panel visualize graph tương tác (D3.js / Cytoscape.js / vis.js) để xem trực quan các liên kết `REQUIRES`, có thể animate quá trình DFS/Dijkstra duyệt qua từng bước.
- Thanh tìm kiếm với autocomplete theo tên Concept/Property.
- Trang quản trị (admin): nhập/sửa Node, Edge, upload file gốc, duyệt đề xuất từ LLM.
- Settings: chọn thuật toán duyệt (DFS/BFS/Dijkstra/A*), cấu hình max-depth.

---

## 7. Chức năng luyện tập & đánh giá

- Module Quiz sinh câu hỏi từ Exercise (thủ công) hoặc từ LLM (tự động), tự động chấm điểm.
- Chế độ "e-Lecture": hiển thị nội dung PDF/DOCX gốc kèm giải thích ngắn gọn.
- Theo dõi tiến độ học cá nhân (Concept nào đã học/chưa học) — dữ liệu nền cho A* cá nhân hóa.

---

## 8. Quản lý người dùng & phân quyền

- Xác thực (đăng nhập) và phân vai trò: **Admin/Giảng viên** (thêm/sửa nội dung, duyệt đề xuất LLM, xây graph) và **Học viên** (tra cứu, làm quiz, xem tiến độ).
- Phân quyền truy cập theo môn học nếu phục vụ nhiều lớp/nhiều giảng viên.
- Lưu lịch sử tra cứu cá nhân (Concept đã xem, quiz đã làm) — bắt buộc để A* cá nhân hóa hoạt động.

---

## 9. Đánh giá chất lượng & độ tin cậy dữ liệu

- Cycle detection trên quan hệ `REQUIRES` (bắt buộc, để tránh DFS/Dijkstra chạy vô hạn).
- Versioning nội dung: giữ lịch sử thay đổi Node/Edge qua từng lần cập nhật, không ghi đè trực tiếp.
- Coverage check: cảnh báo Lesson có Concept nhưng thiếu Property/Exercise/Method (orphan node).

---

## 10. Đo lường & phân tích (Analytics)

- Thống kê Concept được tra cứu nhiều nhất, Exercise học viên làm sai nhiều nhất.
- Dashboard tổng quan tiến độ lớp học cho giảng viên.

---

## 11. Hiệu năng & khả năng mở rộng

- Chỉ mục (indexing) trên Graph DB theo tên Node và theo Subject.
- Giới hạn độ sâu truy vấn để tránh trả kết quả quá rộng.
- Unit test cho các thuật toán duyệt với các trường hợp biên (chu trình, rời rạc, graph sâu).

---

## 12. Tài liệu hóa & bảo trì

- API documentation (Swagger/OpenAPI).
- Changelog cập nhật nội dung graph.
- Cơ chế backup/export graph (JSON/CSV) để không phụ thuộc hoàn toàn vào một Graph DB cụ thể.

---

## 13. Kiến trúc hệ thống tổng thể

```
┌─────────────────────────────────────────────────────────┐
│                     TẦNG GIAO DIỆN                       │
│  Sidebar cây | Panel chi tiết | Graph visualize | Quiz   │
│  Admin panel | Settings (chọn thuật toán, max-depth)     │
└───────────────────────┬───────────────────────────────────┘
                        │ REST / GraphQL API
┌───────────────────────▼───────────────────────────────────┐
│                  TẦNG BACKEND / XỬ LÝ                     │
│  - Module truy vấn: DFS / BFS / Dijkstra / A*             │
│  - Module tìm kiếm từ khóa (full-text + fuzzy)            │
│  - Module LLM: Graph-RAG (Q&A), sinh quiz, giải thích     │
│  - Module Auth & phân quyền                                │
│  - Module Analytics                                        │
└───────────────────────┬───────────────────────────────────┘
                        │
┌───────────────────────▼───────────────────────────────────┐
│                     TẦNG DỮ LIỆU                           │
│  Graph DB (Neo4j / Cypher): Node + Edge như mục 2          │
│  File storage: PDF/DOCX/TXT gốc (Node giữ file_ref)        │
│  Cache: kết quả traversal, câu trả lời LLM theo subgraph   │
└─────────────────────────────────────────────────────────────┘
```

---

## 14. Thứ tự triển khai đề xuất (ưu tiên)

1. Thiết kế schema Graph DB (Node/Edge) + nhập dữ liệu mẫu từ raw data môn AI.
2. Triển khai 4 thuật toán duyệt (DFS/BFS/Dijkstra/A*) + unit test.
3. API tra cứu theo 3 tiêu chí (bài học, phân loại, liên quan).
4. UI cơ bản: sidebar cây + panel chi tiết + tìm kiếm từ khóa.
5. Phân quyền Admin/User + lịch sử tra cứu cá nhân.
6. Cycle detection + coverage check cho chất lượng dữ liệu.
7. Tích hợp LLM: pipeline offline (enrich graph từ PDF/DOCX) trước, pipeline online (Graph-RAG Q&A) sau.
8. Module Quiz (thủ công trước, LLM sinh tự động sau).
9. Graph visualize tương tác + animate traversal.
10. Analytics dashboard + backup/export.
11. Đánh giá độ tin cậy LLM bằng bộ test câu hỏi mẫu (xem mục 15).
12. Hoàn thiện yêu cầu phi chức năng đo lường được (xem mục 16).
13. Chuẩn hóa schema để hỗ trợ đa môn học (xem mục 18).
14. Áp dụng bảo mật/quyền riêng tư + accessibility (xem mục 19).
15. Thiết lập kiểm soát chi phí và observability cho LLM (xem mục 20, 21).
16. Thiết lập CI/CD và chiến lược kiểm thử tổng thể (xem mục 22).

---

## 15. Đánh giá độ tin cậy & kiểm soát chất lượng LLM

- **Faithfulness check:** đảm bảo câu trả lời LLM sinh ra bám sát đúng subgraph đã truy xuất được, không tự thêm thông tin ngoài graph. Cần log lại subgraph input + câu trả lời output để kiểm tra đối chiếu định kỳ.
- **Cơ chế từ chối trả lời (refusal) khi ngoài phạm vi:** nếu câu hỏi không khớp với bất kỳ node nào trong graph, LLM phải trả lời rõ "không có trong tài liệu/graph hiện tại" thay vì tự suy diễn hoặc bịa thông tin.
- **Test riêng cho câu hỏi multi-hop reasoning:** câu hỏi cần đi qua nhiều node liên tiếp có xác suất sai cao hơn câu hỏi tra cứu trực tiếp một node — cần bộ test case riêng, không mặc định LLM xử lý tốt.
- **Bộ câu hỏi kiểm định (evaluation set):** xây dựng trước khi launch một bộ gồm 3 nhóm câu hỏi — (a) factual (tra cứu trực tiếp), (b) reasoning (multi-hop qua REQUIRES), (c) out-of-context (không có trong graph) — để đo Faithfulness và Answer Relevancy, có số liệu cụ thể đưa vào báo cáo đồ án thay vì chỉ mô tả định tính.
- **Giao diện admin duyệt đề xuất LLM khi xây graph:** hiển thị so sánh "trước/sau" (diff view) khi LLM đề xuất thêm Node/Edge mới từ tài liệu, tránh admin approve mù không kiểm tra.

---

## 16. Yêu cầu phi chức năng (đo lường được)

| Hạng mục | Yêu cầu cụ thể (đề xuất, điều chỉnh theo hạ tầng thực tế) |
|---|---|
| Thời gian phản hồi truy vấn graph | DFS/BFS/Dijkstra trả kết quả dưới 500ms cho graph ≤ 1.000 node |
| Thời gian phản hồi LLM (Q&A) | Dưới 3-5 giây cho một câu hỏi Graph-RAG |
| Khả năng chịu lỗi kết nối Graph DB | Hiển thị thông báo lỗi rõ ràng, không crash toàn hệ thống, tự động retry tối đa 3 lần |
| Khả năng chịu lỗi LLM API (timeout/rate-limit) | Fallback trả kết quả graph traversal thuần (không kèm diễn giải LLM) thay vì lỗi trắng trang |
| Giới hạn tải (capacity) | Xác định số node/edge tối đa và số user truy vấn đồng thời hệ thống đảm bảo hiệu năng |
| Tần suất backup dữ liệu | Backup graph tối thiểu hàng ngày, giữ lịch sử tối thiểu 30 ngày |
| Thời gian phục hồi sau lỗi (RTO) | Xác định thời gian tối đa chấp nhận được để khôi phục hệ thống sau sự cố |

---

## 17. Xử lý trường hợp biên & lỗi dữ liệu

- **Graph rỗng/mới khởi tạo:** UI cần trạng thái "chưa có dữ liệu" rõ ràng, không để trắng trang gây hiểu lầm là lỗi.
- **Truy vấn không có kết quả:** thông báo cụ thể (VD: "không tìm thấy khái niệm liên quan") kèm gợi ý từ khóa gần đúng, không trả về danh sách trống không giải thích.
- **File tài liệu lỗi khi xây graph tự động:** xử lý trường hợp PDF quét ảnh không có text layer (cần OCR riêng) hoặc file DOCX hỏng — có log lỗi rõ ràng cho admin, không để pipeline offline chết âm thầm.
- **Trùng lặp dữ liệu:** cơ chế phát hiện Concept/Property trùng tên hoặc trùng ý nghĩa khi LLM đề xuất từ nhiều tài liệu khác nhau, tránh graph phình to với node dư thừa.
- **Xung đột khi nhiều admin sửa cùng lúc:** cơ chế khóa (lock) hoặc cảnh báo conflict khi hai người cùng sửa một Node/Edge.

---

## 18. Khả năng mở rộng sang môn học khác

- Thiết kế schema Node/Edge (mục 2) ở mức **tổng quát hóa** — VD trường `input_file` của Exercise cần đủ chung để chứa cả test case bài lập trình OOP, không chỉ input dạng đồ thị như môn AI.
- Xây dựng khái niệm **"Subject template"**: khi thêm môn học mới, admin chỉ cần định nghĩa lại tập Concept/Property/Exercise riêng cho môn đó thông qua giao diện quản trị, không cần sửa code backend.
- Tách riêng phần **logic thuật toán duyệt** (DFS/BFS/Dijkstra/A*) khỏi **dữ liệu môn học** — đảm bảo thêm môn mới không ảnh hưởng đến module xử lý lõi.
- Xây dựng ít nhất 2 bộ dữ liệu mẫu (VD: môn AI và môn Cấu trúc dữ liệu) để kiểm chứng tính tổng quát của schema trước khi hoàn thiện.

---

## 19. Bảo mật, quyền riêng tư & khả năng tiếp cận

### 19.1. Bảo mật & quyền riêng tư dữ liệu học viên

- **Ẩn danh hóa dữ liệu phân tích:** khi xuất dashboard/analytics cho giảng viên (mục 10), tổng hợp theo nhóm thay vì hiển thị chi tiết hành vi của từng học viên cụ thể.
- **Kiểm soát dữ liệu gửi ra ngoài khi gọi LLM API:** khi dùng LLM cloud cho pipeline Graph-RAG, không gửi thông tin định danh học viên (tên, email) kèm trong prompt — chỉ gửi nội dung tri thức (subgraph).
- **Chính sách lưu trữ và xóa dữ liệu:** quy định rõ thời gian giữ lịch sử tra cứu cá nhân, cơ chế cho học viên yêu cầu xóa dữ liệu của mình.
- **Mã hóa dữ liệu nhạy cảm:** mật khẩu, token xác thực hash/mã hóa đúng chuẩn (bcrypt/argon2), không lưu plaintext.

### 19.2. Khả năng tiếp cận (Accessibility — WCAG 2.1 AA)

- **Điều hướng bằng bàn phím:** sidebar cây, panel graph visualize, quiz phải dùng được không cần chuột.
- **Text alternative cho graph visualize:** node/edge trực quan hóa cần có phiên bản dạng danh sách/text tương đương cho người dùng screen reader.
- **Độ tương phản màu và resize text:** tỷ lệ tương phản đủ chuẩn, text zoom 200% không vỡ layout.
- **Trạng thái lỗi/thông báo rõ ràng cho form:** thông báo lỗi gắn đúng field liên quan, hỗ trợ được bởi screen reader.

---

## 20. Kiểm soát chi phí vận hành LLM

- **Model routing theo độ phức tạp tác vụ:** dùng model rẻ/nhỏ cho tác vụ đơn giản (VD: sinh MCQ cơ bản, tóm tắt ngắn); chỉ dùng model mạnh/đắt cho câu hỏi Graph-RAG phức tạp cần suy luận nhiều bước (multi-hop).
- **Giới hạn độ dài prompt bằng subgraph structured:** vì đã có subgraph từ graph traversal (DFS/Dijkstra), không cần nhồi toàn bộ tài liệu gốc vào prompt — chỉ gửi node/edge liên quan, giữ prompt ngắn và súc tích.
- **Cache system prompt/instruction cố định:** phần hướng dẫn LLM lặp lại mỗi lần gọi (system prompt, format hướng dẫn) nên dùng cơ chế prompt caching của nhà cung cấp để giảm chi phí token đầu vào lặp lại.
- **Cache kết quả theo subgraph (đã có ở mục 5.4):** nhiều câu hỏi có thể trùng subgraph truy xuất — cache câu trả lời theo hash của subgraph để tránh gọi lại LLM không cần thiết.
- **Batching cho tác vụ offline:** khi sinh quiz hàng loạt hoặc enrich graph từ nhiều tài liệu, gộp thành batch request thay vì gọi API từng cái riêng lẻ.
- **Rate limiting theo user:** giới hạn số lượng câu hỏi Graph-RAG mỗi user có thể gửi trong một khoảng thời gian, tránh một user spam gây tốn chi phí không cần thiết.
- **Ngân sách & cảnh báo (budget alert):** đặt ngưỡng chi phí token/tháng theo từng môi trường (dev/staging/production), có cảnh báo tự động khi gần vượt ngưỡng.
- **Theo dõi chi phí theo tác vụ:** phân loại chi phí token theo từng loại tác vụ (Q&A, sinh quiz, xây graph) để biết tác vụ nào tốn nhất, ưu tiên tối ưu đúng chỗ.

---

## 21. Giám sát & theo dõi LLM khi vận hành (LLM Observability)

- **Logging đầy đủ cho mọi lệnh gọi LLM:** ghi lại input (subgraph + câu hỏi), output (câu trả lời), latency, số token, model được dùng cho từng request.
- **Tracing theo luồng xử lý:** với Graph-RAG có nhiều bước (graph traversal → build prompt → gọi LLM → hậu xử lý), cần trace được từng bước để debug khi có lỗi, không chỉ thấy kết quả cuối.
- **Evaluation tự động kết hợp 2 lớp:** lớp 1 — kiểm tra định dạng/heuristic (format hợp lệ, không chứa từ cấm) chạy trên 100% traffic; lớp 2 — LLM-as-judge chấm điểm ngữ nghĩa (đúng/liên quan/bám sát graph) chạy trên mẫu 5-20% traffic để không tốn thêm quá nhiều chi phí.
- **Thu thập phản hồi người dùng:** nút like/dislike hoặc "câu trả lời này có đúng không" ngay trên UI Q&A, dùng làm tín hiệu thời gian thực để phát hiện vấn đề nhanh hơn eval tự động.
- **Dashboard theo dõi theo thời gian:** trực quan hóa latency, tỷ lệ lỗi, điểm chất lượng (faithfulness/relevancy) theo thời gian, có ngưỡng cảnh báo khi vượt mức cho phép.
- **Phát hiện drift:** theo dõi khi chất lượng câu trả lời giảm dần theo thời gian (VD: do graph cập nhật nhiều nội dung mới mà prompt/logic chưa theo kịp), dùng dữ liệu này để tinh chỉnh lại pipeline.
- **Xây dựng bộ test hồi quy (regression test) từ lỗi thực tế:** khi phát hiện một câu trả lời sai trong production, thêm case đó vào bộ eval offline để đảm bảo lỗi tương tự không lặp lại ở lần cập nhật sau.

---

## 22. CI/CD & chiến lược kiểm thử tổng thể

- **Pipeline CI cơ bản:** tự động chạy lint, type-check, unit test cho mọi commit; không cho merge nếu test bắt buộc chưa pass hoặc đang lỗi thời (stale).
- **Tách môi trường:** tối thiểu 3 môi trường Development → Staging → Production; deploy đúng artifact đã build một lần, không build lại riêng cho từng môi trường.
- **Test riêng cho phần thuật toán (deterministic):** unit test cho DFS/BFS/Dijkstra/A* với input cố định, kỳ vọng output chính xác 100% — coverage cao, vì đây là phần logic có thể kiểm chứng tuyệt đối.
- **Test riêng cho phần LLM (probabilistic):** dùng bộ eval set (mục 15) đo theo ngưỡng chất lượng (VD: Faithfulness ≥ 0.85), không kỳ vọng đúng 100% như test thuật toán.
- **Test tích hợp (integration test):** kiểm tra luồng đầy đủ từ UI → API → Graph DB → (nếu có) LLM, đảm bảo các module ghép nối đúng, không chỉ test riêng từng phần.
- **Chiến lược deploy an toàn:** dùng canary hoặc rolling deployment khi đưa bản cập nhật lên production, tránh đẩy thẳng 100% traffic vào bản mới chưa kiểm chứng.
- **Kế hoạch rollback:** xác định rõ điều kiện nào (tỷ lệ lỗi tăng, latency vượt ngưỡng) sẽ kích hoạt rollback, và đảm bảo có thể rollback nhanh (dưới vài phút).
- **Migration database an toàn:** khi thay đổi schema Graph DB, đảm bảo tương thích ngược (backward-compatible) trong giai đoạn chuyển đổi, tránh mất dữ liệu hoặc downtime.

---
---

# PHẦN II — SPEC KỸ THUẬT THI HÀNH ĐƯỢC

## 23. Quyết định Stack công nghệ (đã chốt)

| Thành phần | Lựa chọn | Lý do |
|---|---|---|
| Backend | Node.js + Express | Một ngôn ngữ cho cả traversal logic và API, dễ tích hợp Neo4j driver + LLM SDK |
| Database chính | Neo4j (Cypher) | Đúng bài toán graph, hỗ trợ traversal algorithm sẵn có để đối chiếu kết quả tự code |
| Frontend | React + Cytoscape.js | Cytoscape có layout algorithm sẵn, mạnh hơn D3 cho việc thao tác graph tương tác |
| LLM | OpenAI API (model có thể đổi qua config) | Phổ biến, nhiều tài liệu, dễ swap sang model khác sau |
| Auth | JWT + bcrypt | Đơn giản, đủ dùng cho quy mô đồ án/hệ thống nhỏ |
| Full-text search | Neo4j full-text index (Lucene-based) | Không cần thêm Elasticsearch riêng ở giai đoạn MVP |

**Ghi chú:** nếu hạ tầng triển khai thực tế không có Neo4j (VD chỉ có PostgreSQL), có thể thay bằng mô hình adjacency list trong bảng `edges (from_id, to_id, type, weight)` — toàn bộ pseudocode thuật toán ở mục 25 vẫn áp dụng được, chỉ đổi câu truy vấn lấy neighbor.

---

## 24. Phạm vi MVP (làm trước) vs Giai đoạn 2 (làm sau)

**MVP — bắt buộc có trong bản đầu tiên:**
- Data model (Node/Edge) + import dữ liệu mẫu môn AI.
- 3 loại tra cứu: theo bài học, theo phân loại, theo kiến thức liên quan.
- 4 thuật toán duyệt: DFS, BFS, Dijkstra, A* — chọn được qua tham số API.
- UI: sidebar cây, panel chi tiết node, tìm kiếm từ khóa cơ bản, visualize graph đơn giản.
- Auth cơ bản: 2 vai trò Admin/User.
- Cycle detection khi tạo cạnh REQUIRES.

**Giai đoạn 2 — sau khi MVP chạy ổn:**
- Tích hợp LLM (Graph-RAG Q&A, sinh quiz tự động, xây graph từ PDF/DOCX).
- Analytics dashboard, versioning, coverage check.
- Accessibility (WCAG AA), bảo mật nâng cao, cost control, observability.
- CI/CD đầy đủ, multi-subject template.

---

## 25. Schema dữ liệu cụ thể (Cypher — sẵn sàng chạy)

### 25.1. Ràng buộc & Index (chạy trước khi insert data)

```cypher
CREATE CONSTRAINT subject_id_unique IF NOT EXISTS FOR (s:Subject) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT lesson_id_unique IF NOT EXISTS FOR (l:Lesson) REQUIRE l.id IS UNIQUE;
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT property_id_unique IF NOT EXISTS FOR (p:Property) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT exercise_id_unique IF NOT EXISTS FOR (e:Exercise) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT method_id_unique IF NOT EXISTS FOR (m:Method) REQUIRE m.id IS UNIQUE;

CREATE FULLTEXT INDEX conceptSearch IF NOT EXISTS FOR (c:Concept) ON EACH [c.name, c.description];
CREATE FULLTEXT INDEX propertySearch IF NOT EXISTS FOR (p:Property) ON EACH [p.statement];
```

### 25.2. Dữ liệu mẫu — import trực tiếp từ raw data môn AI đã cung cấp

```cypher
// ===== NODES =====
CREATE (subj:Subject {id: 'subj_ai', name: 'Tri tue nhan tao', description: 'Mon hoc AI'})

CREATE (l1:Lesson {id: 'lesson_overview', title: 'Khai niem nen tang', file_ref: '1. Tong quan ve TTNT.pdf', order: 1})
CREATE (l2:Lesson {id: 'lesson_heuristic', title: 'Tim kiem kinh nghiem', file_ref: '2. Thuat giai Heuristic.pdf', order: 2})
CREATE (l3:Lesson {id: 'lesson_search', title: 'Khong gian trang thai va Tim kiem mu', file_ref: '3. Phuong phap tim kiem.pdf', order: 3})
CREATE (l4:Lesson {id: 'lesson_minimax', title: 'Tim kiem doi khang', file_ref: '4. Chien luoc Minimax.doc', order: 4})
CREATE (l5:Lesson {id: 'lesson_kr', title: 'Bieu dien tri thuc', file_ref: '5, 6a BDTT.pdf', order: 5})

CREATE (c1:Concept {id: 'concept_dfs', name: 'Tim kiem theo chieu sau (DFS)', description: '...', difficulty_level: 2})
CREATE (c2:Concept {id: 'concept_dijkstra', name: 'Thuat toan Dijkstra', description: '...', difficulty_level: 3})
CREATE (c3:Concept {id: 'concept_astar', name: 'Thuat giai A*', description: '...', difficulty_level: 4})
CREATE (c4:Concept {id: 'concept_heuristic', name: 'Ham Heuristic', description: '...', difficulty_level: 2})
CREATE (c5:Concept {id: 'concept_minimax', name: 'Chien luoc Minimax', description: '...', difficulty_level: 4})
CREATE (c6:Concept {id: 'concept_logic', name: 'Logic menh de', description: '...', difficulty_level: 2})

CREATE (p1:Property {id: 'prop_dfs', statement: 'Khong dam bao tinh toi uu, de lap vo han', latex_formula: null})
CREATE (p2:Property {id: 'prop_dijkstra', statement: 'Tim duong di ngan nhat, trong so khong am', latex_formula: null})
CREATE (p3:Property {id: 'prop_astar', statement: 'Ham danh gia', latex_formula: 'f(n) = g(n) + h(n)'})

CREATE (e1:Exercise {id: 'ex_dfs_graph', description: 'Duyet do thi', input_file: 'DothiSearch.txt', difficulty: 2})
CREATE (e2:Exercise {id: 'ex_dijkstra_graph', description: 'Tim duong di do thi co trong so', input_file: 'DothiDijkstra.txt', difficulty: 3})
CREATE (e3:Exercise {id: 'ex_astar_graph', description: 'Bai toan tim duong di toi uu', input_file: 'DothiAStart.txt', difficulty: 4})
CREATE (e4:Exercise {id: 'ex_minimax_game', description: 'Co Caro, Tic-Tac-Toe, Co vua', input_file: null, difficulty: 4})
CREATE (e5:Exercise {id: 'ex_logic_proof', description: 'Chung minh he qua logic', input_file: null, difficulty: 2})

CREATE (m1:Method {id: 'method_dfs', code_file: 'DFS.docx', language: 'C++/Java', complexity_note: 'O(V+E)'})
CREATE (m2:Method {id: 'method_dijkstra', code_file: 'Dijkstra.docx', language: 'C++/Java', complexity_note: 'O(E log V)'})
CREATE (m3:Method {id: 'method_astar', code_file: 'AStart.docx', language: 'C++/Java', complexity_note: 'O(E) voi heuristic tot'})
CREATE (m4:Method {id: 'method_logic', code_file: 'Mau BT Logic menh de.pdf', language: null, complexity_note: null})

// ===== EDGES =====
CREATE (subj)-[:HAS_LESSON]->(l1)
CREATE (subj)-[:HAS_LESSON]->(l2)
CREATE (subj)-[:HAS_LESSON]->(l3)
CREATE (subj)-[:HAS_LESSON]->(l4)
CREATE (subj)-[:HAS_LESSON]->(l5)

CREATE (l3)-[:INCLUDES]->(c1)
CREATE (l3)-[:INCLUDES]->(c2)
CREATE (l2)-[:INCLUDES]->(c3)
CREATE (l2)-[:INCLUDES]->(c4)
CREATE (l4)-[:INCLUDES]->(c5)
CREATE (l5)-[:INCLUDES]->(c6)

CREATE (c1)-[:HAS_PROPERTY]->(p1)
CREATE (c2)-[:HAS_PROPERTY]->(p2)
CREATE (c3)-[:HAS_PROPERTY]->(p3)

CREATE (c1)-[:APPLIED_IN]->(e1)
CREATE (c2)-[:APPLIED_IN]->(e2)
CREATE (c3)-[:APPLIED_IN]->(e3)
CREATE (c5)-[:APPLIED_IN]->(e4)
CREATE (c6)-[:APPLIED_IN]->(e5)

CREATE (e1)-[:SOLVED_BY]->(m1)
CREATE (e2)-[:SOLVED_BY]->(m2)
CREATE (e3)-[:SOLVED_BY]->(m3)
CREATE (e5)-[:SOLVED_BY]->(m4)

// REQUIRES - trong so mac dinh the hien do "nang" cua kien thuc tien quyet
CREATE (c3)-[:REQUIRES {weight: 1}]->(c4)
CREATE (c3)-[:REQUIRES {weight: 2}]->(c2)
CREATE (c5)-[:REQUIRES {weight: 1}]->(c1)
```

**Lưu ý cho agent:** file gốc PDF/DOCX/TXT (VD `DothiAStart.txt`, `AStart.docx`) **không lưu trong Neo4j** — chỉ lưu đường dẫn/tên file ở trường `file_ref`/`code_file`/`input_file`. File thật lưu trên file storage (local disk trong giai đoạn MVP, S3-compatible storage nếu triển khai thật).

---

## 26. Pseudocode thuật toán duyệt Graph (spec hàm cụ thể)

### 26.1. Nguyên tắc chung — input/output contract thống nhất

```
Input:
  start_node_id: string       // node bắt đầu (Concept id)
  algorithm: 'dfs' | 'bfs' | 'dijkstra' | 'astar'
  max_depth: number           // giới hạn độ sâu, default = 5
  target_node_id?: string     // bắt buộc với dijkstra/astar, optional với dfs/bfs

Output:
  {
    visited_order: [node_id],       // thứ tự duyệt qua
    path?: [node_id],               // đường đi từ start đến target (chỉ dijkstra/astar)
    total_cost?: number,            // tổng trọng số đường đi (chỉ dijkstra/astar)
    depth_reached: number,
    cycle_detected: boolean
  }
```

### 26.2. DFS — liệt kê kiến thức tiên quyết theo nhánh sâu

```
function dfsTraverse(startNodeId, maxDepth):
    visited = new Set()
    order = []
    cycleDetected = false

    function dfsVisit(nodeId, depth, pathStack):
        if depth > maxDepth: return
        if nodeId in pathStack:          // phat hien chu trinh
            cycleDetected = true
            return
        if nodeId in visited: return

        visited.add(nodeId)
        order.append(nodeId)
        pathStack.add(nodeId)

        neighbors = getNeighbors(nodeId, edgeType='REQUIRES')  // query Cypher
        for neighbor in neighbors:
            dfsVisit(neighbor.id, depth + 1, pathStack)

        pathStack.remove(nodeId)          // backtrack

    dfsVisit(startNodeId, 0, new Set())
    return { visited_order: order, depth_reached: maxDepthUsed, cycle_detected: cycleDetected }
```

**Cypher lấy neighbor tương ứng:**
```cypher
MATCH (n:Concept {id: $nodeId})-[:REQUIRES]->(m:Concept)
RETURN m.id AS id, m.name AS name
```

### 26.3. BFS — liệt kê kiến thức liên quan theo từng lớp gần-xa

```
function bfsTraverse(startNodeId, maxDepth):
    visited = new Set([startNodeId])
    queue = [(startNodeId, 0)]
    order = []

    while queue is not empty:
        (nodeId, depth) = queue.dequeue()
        if depth > maxDepth: continue
        order.append({ id: nodeId, depth: depth })

        neighbors = getNeighbors(nodeId, edgeType='REQUIRES')
        for neighbor in neighbors:
            if neighbor.id not in visited:
                visited.add(neighbor.id)
                queue.enqueue((neighbor.id, depth + 1))

    return { visited_order: order, depth_reached: maxDepthActual, cycle_detected: false }
    // BFS voi visited-set khong bao gio lap vo han, nhung van nen bao cao
    // canh REQUIRES nao tao cycle rieng qua ham detectCycle() o muc 26.6
```

### 26.4. Dijkstra — lộ trình học "nhẹ nhất" đến kiến thức mục tiêu

```
function dijkstra(startNodeId, targetNodeId, maxDepth):
    dist = { startNodeId: 0 }
    prev = {}
    priorityQueue = new MinHeap()
    priorityQueue.push((0, startNodeId))
    visitedOrder = []

    while priorityQueue is not empty:
        (currentDist, nodeId) = priorityQueue.popMin()
        if nodeId in visitedOrder: continue
        visitedOrder.append(nodeId)

        if nodeId == targetNodeId:
            break

        neighbors = getNeighborsWithWeight(nodeId, edgeType='REQUIRES')
        for (neighborId, weight) in neighbors:
            newDist = currentDist + weight
            if neighborId not in dist or newDist < dist[neighborId]:
                dist[neighborId] = newDist
                prev[neighborId] = nodeId
                priorityQueue.push((newDist, neighborId))

    path = reconstructPath(prev, startNodeId, targetNodeId)
    return {
        visited_order: visitedOrder,
        path: path,
        total_cost: dist.get(targetNodeId, Infinity),
        cycle_detected: false
    }
```

**Cypher lấy neighbor kèm trọng số:**
```cypher
MATCH (n:Concept {id: $nodeId})-[r:REQUIRES]->(m:Concept)
RETURN m.id AS id, r.weight AS weight
```

### 26.5. A\* — lộ trình cá nhân hóa (nâng cao)

```
function aStar(startNodeId, targetNodeId, maxDepth, userMasteryMap):
    // heuristic: uoc luong "con bao nhieu kien thuc con thieu" tu userMasteryMap
    function heuristic(nodeId):
        if userMasteryMap[nodeId] == true: return 0   // da biet -> khong tinh vao chi phi con lai
        return estimateRemainingDepth(nodeId, targetNodeId)  // BFS ngan tu nodeId den targetNodeId, khong tinh weight

    gScore = { startNodeId: 0 }
    fScore = { startNodeId: heuristic(startNodeId) }
    openSet = new MinHeap()
    openSet.push((fScore[startNodeId], startNodeId))
    prev = {}
    visitedOrder = []

    while openSet is not empty:
        (_, nodeId) = openSet.popMin()
        visitedOrder.append(nodeId)
        if nodeId == targetNodeId:
            break

        neighbors = getNeighborsWithWeight(nodeId, edgeType='REQUIRES')
        for (neighborId, weight) in neighbors:
            tentativeG = gScore[nodeId] + weight
            if neighborId not in gScore or tentativeG < gScore[neighborId]:
                gScore[neighborId] = tentativeG
                fScore[neighborId] = tentativeG + heuristic(neighborId)
                prev[neighborId] = nodeId
                openSet.push((fScore[neighborId], neighborId))

    path = reconstructPath(prev, startNodeId, targetNodeId)
    return {
        visited_order: visitedOrder,
        path: path,
        total_cost: gScore.get(targetNodeId, Infinity),
        cycle_detected: false
    }
```

### 26.6. Cycle Detection (chạy khi Admin tạo cạnh REQUIRES mới)

```
function detectCycle(newEdgeFrom, newEdgeTo):
    // kiem tra: neu them canh (newEdgeFrom -> newEdgeTo) co tao chu trinh khong
    // = kiem tra co duong di tu newEdgeTo quay lai newEdgeFrom hay khong (DFS)
    visited = new Set()

    function hasPath(fromId, toId):
        if fromId == toId: return true
        visited.add(fromId)
        neighbors = getNeighbors(fromId, edgeType='REQUIRES')
        for neighbor in neighbors:
            if neighbor.id not in visited:
                if hasPath(neighbor.id, toId): return true
        return false

    return hasPath(newEdgeTo, newEdgeFrom)   // true = se tao chu trinh, tu choi tao canh
```

---

## 27. API Contract (endpoint cụ thể cho MVP)

### 27.1. Tra cứu theo bài học

```
GET /api/subjects/:subjectId/lessons
Response 200:
[
  { "id": "lesson_search", "title": "Khong gian trang thai va Tim kiem mu", "order": 3 }
]

GET /api/lessons/:lessonId/concepts
Response 200:
[
  { "id": "concept_dfs", "name": "Tim kiem theo chieu sau (DFS)", "difficulty_level": 2 }
]
```

### 27.2. Tra cứu theo phân loại

```
GET /api/concepts/:conceptId/properties
GET /api/concepts/:conceptId/exercises
GET /api/exercises/:exerciseId/methods
```

### 27.3. Tra cứu theo kiến thức liên quan (endpoint lõi — dùng thuật toán)

```
GET /api/concepts/:conceptId/related?algorithm=dfs&max_depth=5
GET /api/concepts/:conceptId/related?algorithm=bfs&max_depth=3
GET /api/concepts/:conceptId/path?algorithm=dijkstra&target=concept_astar
GET /api/concepts/:conceptId/path?algorithm=astar&target=concept_astar&user_id=u123

Response 200 (mau cho dijkstra/astar):
{
  "visited_order": ["concept_astar", "concept_heuristic", "concept_dijkstra"],
  "path": ["concept_astar", "concept_dijkstra"],
  "total_cost": 2,
  "depth_reached": 2,
  "cycle_detected": false
}
```

### 27.4. Tìm kiếm từ khóa

```
GET /api/search?q=A*&type=concept&subject=subj_ai
Response 200:
[
  { "id": "concept_astar", "name": "Thuat giai A*", "type": "Concept", "score": 0.95 }
]
```

### 27.5. Admin — tạo/sửa Node/Edge

```
POST /api/admin/concepts
Body: { "id": "concept_new", "name": "...", "lesson_id": "lesson_search" }

POST /api/admin/edges
Body: { "from": "concept_new", "to": "concept_dfs", "type": "REQUIRES", "weight": 1 }
Response 409 (neu detectCycle() = true):
{ "error": "Thao tac nay se tao chu trinh trong quan he REQUIRES" }
```

---

## 28. Wireframe mô tả (thay cho hình vẽ)

### 28.1. Layout tổng thể (3 cột)

```
+------------------+---------------------------+------------------------+
|  SIDEBAR CAY     |    PANEL CHI TIET NODE    |   PANEL GRAPH VISUALIZE|
|  (trai, 20%)     |    (giua, 45%)            |   (phai, 35%)          |
|                  |                           |                        |
| Subject: AI      | [Ten Concept]             |   (Cytoscape.js canvas)|
|  > Lesson 1      | [Do kho] [Bai hoc goc]    |   node = concept       |
|  > Lesson 2      |                           |   canh mau do = REQUIRES|
|    - Concept A   | Tab: [Tinh chat]          |   click node -> load   |
|    - Concept B   |      [Bai tap]            |   sang panel giua      |
|  > Lesson 3      |      [Phuong phap giai]   |                        |
|                  |      [Kien thuc lien quan]|   Setting (goc tren):  |
| [Thanh tim kiem] |                           |   Thuat toan: [DFS v]  |
+------------------+---------------------------+------------------------+
```

### 28.2. Tab "Kiến thức liên quan" trong Panel chi tiết

- Dropdown chọn thuật toán: DFS / BFS / Dijkstra / A*.
- Input số: max_depth (default 5).
- Nếu chọn Dijkstra/A*: thêm dropdown chọn Concept đích (target).
- Nút "Tra cứu" → gọi API mục 27.3 → hiển thị kết quả dạng danh sách + highlight trên Panel Graph Visualize bên phải.

### 28.3. Trang Admin (route riêng `/admin`)

- Bảng danh sách Node theo từng loại (tab Subject/Lesson/Concept/Property/Exercise/Method).
- Nút "Thêm mới" mở modal form theo schema tương ứng.
- Khi thêm cạnh REQUIRES: nếu backend trả lỗi 409 (cycle), hiển thị thông báo đỏ ngay trên form, không cho submit.

---

## 29. Cấu trúc thư mục project đề xuất

```
project-root/
├── backend/
│   ├── src/
│   │   ├── algorithms/          # dfs.js, bfs.js, dijkstra.js, astar.js, cycleDetect.js
│   │   ├── db/                  # neo4j connection, cypher queries
│   │   ├── routes/               # subjects.js, concepts.js, search.js, admin.js
│   │   ├── controllers/
│   │   ├── models/               # schema validation (Joi/Zod)
│   │   └── app.js
│   ├── tests/                    # unit test cho tung thuat toan (muc 26)
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── components/           # Sidebar, DetailPanel, GraphVisualize, SearchBar
│   │   ├── pages/                # Home, Admin
│   │   ├── api/                  # gọi API backend
│   │   └── App.jsx
│   └── package.json
├── data/
│   └── seed_ai_subject.cypher    # noi dung muc 25.2
└── docs/
    └── he-thong-tra-cuu-kien-thuc-full-plan.md
```

---

## 30. Checklist cho agent trước khi bắt đầu

- [ ] Cài Neo4j (local hoặc Neo4j Aura free tier), chạy script mục 25.1 và 25.2.
- [ ] Khởi tạo backend Node.js + Express, kết nối Neo4j qua driver `neo4j-driver`.
- [ ] Code 4 module thuật toán theo pseudocode mục 26, viết unit test trước khi nối API.
- [ ] Code cycle detection, gắn vào endpoint tạo cạnh REQUIRES (mục 27.5).
- [ ] Code các endpoint API theo đúng contract mục 27.
- [ ] Khởi tạo frontend React, dựng layout 3 cột theo wireframe mục 28.
- [ ] Tích hợp Cytoscape.js, test hiển thị đúng dữ liệu mẫu môn AI.
- [ ] Auth cơ bản (JWT) + 2 route bảo vệ: `/admin/*` chỉ cho role admin.
- [ ] Sau khi MVP chạy ổn, mới quay lại các mục Giai đoạn 2 (mục 5, 15-22 ở Phần I).

---

*Tài liệu tổng hợp từ toàn bộ quá trình brainstorm, gộp Plan (Phần I) và Spec kỹ thuật (Phần II) thành một file duy nhất để giao cho AI agent / lập trình viên triển khai.*
