(Subject): Trí tuệ nhân tạo (AI)
 │
 ├── [HAS_LESSON] ──> (Lesson): Khái niệm nền tảng (File: 1. Tong quan ve TTNT.pdf)
 │
 ├── [HAS_LESSON] ──> (Lesson): Không gian trạng thái & Tìm kiếm mù (File: 3. Phuong phap tim kiem.pdf)
 │    │
 │    ├── [INCLUDES] ──> (Concept): Tìm kiếm theo chiều sâu (DFS)
 │    │    │
 │    │    ├── [HAS_PROPERTY] ──> (Property): Không đảm bảo tính tối ưu, dễ lặp vô hạn
 │    │    └── [APPLIED_IN] ────> (Exercise): Duyệt đồ thị (Input: DothiSearch.txt)
 │    │         └── [SOLVED_BY] ──> (Method): Mã nguồn DFS (File: DFS.docx)
 │    │
 │    └── [INCLUDES] ──> (Concept): Thuật toán Dijkstra
 │         │
 │         ├── [HAS_PROPERTY] ──> (Property): Tìm đường đi ngắn nhất, trọng số không âm
 │         └── [APPLIED_IN] ────> (Exercise): Tìm đường đi đồ thị có trọng số (Input: DothiDijkstra.txt)
 │              └── [SOLVED_BY] ──> (Method): Mã nguồn Dijkstra (File: Dijkstra.docx)
 │
 ├── [HAS_LESSON] ──> (Lesson): Tìm kiếm kinh nghiệm (File: 2. Thuat giai Heuristic.pdf)
 │    │
 │    └── [INCLUDES] ──> (Concept): Thuật giải A*
 │         │
 │         │── Yêu cầu 3: KẾT NỐI KIẾN THỨC BẮT BUỘC & LIÊN QUAN ──────────
 │         ├── [REQUIRES] ──────> (Concept): Hàm Heuristic (Từ Bài 2)
 │         ├── [REQUIRES] ──────> (Concept): Thuật toán Dijkstra (Từ Bài 3)
 │         │
 │         ├── [HAS_PROPERTY] ──> (Property): Hàm đánh giá $f(n) = g(n) + h(n)$
 │         │
 │         └── [APPLIED_IN] ────> (Exercise): Bài toán tìm đường đi tối ưu (Input: DothiAStart.txt)
 │              └── [SOLVED_BY] ──> (Method): Mã nguồn C++/Java (File: AStart.docx)
 │
 ├── [HAS_LESSON] ──> (Lesson): Tìm kiếm đối kháng
 │    └── [INCLUDES] ──> (Concept): Chiến lược Minimax (File: 4. Chien luoc Minimax.doc)
 │         │
 │         ├── [REQUIRES] ──────> (Concept): Tìm kiếm theo chiều sâu (DFS)  <══ Liên kết chéo
 │         └── [APPLIED_IN] ────> (Exercise): Cờ Caro, Tic-Tac-Toe, Cờ vua
 │
 └── [HAS_LESSON] ──> (Lesson): Biểu diễn tri thức (File: 5, 6a BDTT.pdf, 2023.5)
      └── [INCLUDES] ──> (Concept): Logic mệnh đề
           └── [APPLIED_IN] ────> (Exercise): Chứng minh hệ quả logic
                └── [SOLVED_BY] ──> (Method): Phương pháp giải mẫu (File: Mau BT Logic menh de.pdf)