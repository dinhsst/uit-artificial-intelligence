# Bài giải Bài tập 3 — Thuật giải A*

## Tệp trong bộ bài

- `LOI GIAI BAI TAP 3.tex`: lời giải chi tiết hai bài bằng LaTeX.
- `astar_8puzzle.py`: chương trình giải 8-puzzle bằng A*.
- `INPUT.txt`: input mẫu đúng theo đề.
- `OUTPUT.txt`: tệp output được chương trình sinh ra sau khi chạy.
- `8puzzle_mophong.html`: mô phỏng tương tác chạy trực tiếp trên trình duyệt, không cần máy chủ.

## Chạy chương trình

Yêu cầu Python 3.8 trở lên. Tạo môi trường ảo rồi chạy chương trình:

```text
py -m venv .venv
.\.venv\Scripts\python.exe astar_8puzzle.py
```

Mặc định chương trình đọc `INPUT.txt` và ghi `OUTPUT.txt`. Có thể chỉ định
hai đường dẫn:

```text
.\.venv\Scripts\python.exe astar_8puzzle.py INPUT.txt OUTPUT.txt
```

Chương trình chỉ dùng thư viện chuẩn, không cần cài thêm gói nào.

## Định dạng INPUT.txt

```text
3
2 8 3
1 6 4
7 0 5
1 2 3
8 0 4
7 6 5
```

Dòng đầu là kích thước bàn cờ. Ba dòng tiếp theo là trạng thái đầu và ba
dòng cuối là trạng thái đích. Số `0` là ô trống. Chương trình kiểm tra
kích thước, số lượng dòng và hoán vị các số từ 0 đến 8.

## Thuật toán

- A* với priority queue `heapq`.
- `g`: số nước đi từ trạng thái đầu.
- `h`: tổng khoảng cách Manhattan của các quân khác 0 đến vị trí đích.
- `f = g + h`.
- Bảng `best_g` loại bỏ các đường đi kém hơn đến cùng một trạng thái.
- Parity nghịch thế được kiểm tra trước để phát hiện bài toán không khả giải.

Mã nước đi theo hướng di chuyển của ô trống: `U` = Lên, `D` = Xuống,
`L` = Trái, `R` = Phải.

## Kết quả Bài 1

Đường đi A* tối ưu trên bản đồ Romania:

`Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest`

Tổng chi phí: `417 km`.

