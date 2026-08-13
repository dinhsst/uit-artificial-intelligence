# Phân công luận văn — Cân bằng tải & tối thiểu makespan

## Ý tưởng

Cho 12 luận văn với số trang khác nhau, cần phân về các nhân viên sao cho **thời gian hoàn thành lâu nhất** (`makespan` = max của `pages / speed`) là nhỏ nhất. Đây là bài toán scheduling / load balancing thuộc lớp NP-hard, nên chương trình dùng heuristic tham lam, ở Câu B kết hợp thêm tìm kiếm cục bộ.

Mỗi worker là một dict `{"Name", "speed", "jobs", "pages"}`; `luan_van_tuple` là danh sách `(tên, số_trang)` đã sắp xếp giảm dần theo số trang.

## Câu A — Tham lam LPT

Ba nhân viên cùng tốc độ. Sắp xếp luận văn giảm dần theo số trang (*Longest Processing Time first*), rồi lần lượt gán mỗi luận văn cho nhân viên đang **ít trang nhất**.

```python
# Sắp xếp giảm dần: việc lớn được đặt trước, khi còn nhiều dư địa cân bằng
luan_van_tuple.sort(key=lambda item: item[1], reverse=True)

workers = [{"Name": "W1", "jobs": [], "pages": 0},
           {"Name": "W2", "jobs": [], "pages": 0},
           {"Name": "W3", "jobs": [], "pages": 0}]

for luan_van in luan_van_tuple:
    # Cùng tốc độ ⇒ cân bằng số trang chính là cân bằng thời gian.
    # Sắp workers tăng dần theo pages rồi lấy người ít trang nhất.
    workers.sort(key=lambda item: item["pages"])
    min_worker = workers[0]

    # Gán luận văn hiện tại cho người "rảnh" nhất
    min_worker["jobs"].append(luan_van[0])
    min_worker["pages"] += luan_van[1]
```

**Giải thích:** mỗi bước chọn `min_worker` (người ít trang nhất) để nhận việc kế tiếp nên tải được san đều dần. Vì tốc độ đồng đều, tối thiểu số trang lớn nhất cũng là tối thiểu makespan.

## Câu B — Tốc độ không đồng đều + local search

Thêm một *Manager* với tốc độ bằng một nửa (`speed = 4` so với `8`), nên cân bằng theo số trang không còn đúng — phải cân bằng theo **thời gian** `pages / speed`. Thuật toán gồm hai giai đoạn: khởi tạo tham lam rồi cải thiện bằng tìm kiếm cục bộ.

### Giai đoạn 1 — khởi tạo tham lam

```python
workers = [{"Name": "W1", "speed": 8, "jobs": [], "pages": 0},
           {"Name": "W2", "speed": 8, "jobs": [], "pages": 0},
           {"Name": "W3", "speed": 8, "jobs": [], "pages": 0},
           {"Name": "Manager", "speed": 4, "jobs": [], "pages": 0}]

for luan_van in luan_van_tuple:
    # Sắp theo GIỜ hoàn thành nếu nhận thêm việc này: (pages + trang_mới) / speed.
    # Nhờ chia cho speed, Manager (chậm) tự động được dồn ít việc hơn.
    workers.sort(key=lambda item: (item["pages"] + luan_van[1]) / item["speed"])
    min_worker = workers[0]

    min_worker["jobs"].append(luan_van[0])
    min_worker["pages"] += luan_van[1]
```

### Giai đoạn 2 — tìm kiếm cục bộ (hill climbing)

```python
def makespan(workers):
    # Thời gian hoàn thành = worker lâu nhất
    return max(w["pages"] / w["speed"] for w in workers)


def all_neighbors(workers):
    # Sinh mọi "trạng thái lân cận" chỉ khác trạng thái hiện tại một thao tác nhỏ
    neighbors = []
    trang = dict(luan_van_tuple)          # tra cứu nhanh: tên_luận_văn -> số trang

    # (i) MOVE: chuyển 1 luận văn từ worker a sang worker b
    for a in range(len(workers)):
        for job in list(workers[a]["jobs"]):
            for b in range(len(workers)):
                if b != a:
                    new_workers = copy.deepcopy(workers)   # tránh sửa nhầm bản gốc
                    new_workers[b]["jobs"].append(job)
                    new_workers[a]["jobs"].remove(job)
                    new_workers[a]["pages"] -= trang[job]
                    new_workers[b]["pages"] += trang[job]
                    neighbors.append(new_workers)

    # (ii) SWAP: đổi chỗ luận văn job của a với luận văn c của b
    for a in range(len(workers)):
        for job in workers[a]["jobs"]:
            for b in range(a + 1, len(workers)):     # a < b để không lặp cặp
                for c in workers[b]["jobs"]:
                    new_workers = copy.deepcopy(workers)
                    new_workers[a]["jobs"].remove(job)
                    new_workers[a]["jobs"].append(c)
                    new_workers[b]["jobs"].remove(c)
                    new_workers[b]["jobs"].append(job)
                    new_workers[a]["pages"] += trang[c] - trang[job]
                    new_workers[b]["pages"] += trang[job] - trang[c]
                    neighbors.append(new_workers)
    return neighbors


def local_search(workers):
    while True:
        cai_thien = False
        makespan_hien_tai = makespan(workers)

        for neighbor in all_neighbors(workers):
            # First-improvement: nhận NGAY lân cận đầu tiên tốt hơn
            if makespan(neighbor) < makespan_hien_tai:
                workers = neighbor
                cai_thien = True
                break

        # Duyệt hết lân cận mà không cải thiện được nữa ⇒ cực tiểu cục bộ, dừng
        if not cai_thien:
            break

    return workers
```

**Giải thích:**

- **Khởi tạo tham lam** sắp theo `(pages + luan_van[1]) / speed` nên tự động dồn ít việc hơn cho `Manager` — cho một điểm xuất phát hợp lý.
- `all_neighbors` coi mỗi phương án phân công là một trạng thái; lân cận là phương án chỉ khác một thao tác **MOVE** (dời một việc) hoặc **SWAP** (đổi hai việc). Dùng cả hai vì chỉ *move* đôi khi bị kẹt, còn *swap* tinh chỉnh được mà không đổi số việc mỗi người.
- `local_search` lặp lại việc nhảy sang lân cận đầu tiên có makespan nhỏ hơn (*first-improvement*), dừng khi `cai_thien` vẫn `False` — tức đạt **cực tiểu cục bộ**. Không đảm bảo tối ưu toàn cục nhưng thường tốt hơn hẳn kết quả tham lam ban đầu.

Kết quả in qua `in_ket_qua` gồm phân công, số trang, số giờ mỗi người và makespan tổng.

## Hướng dẫn sử dụng

Chỉ dùng thư viện chuẩn (`copy`), không cần cài thêm gói nào:

```bash
python main.py
```