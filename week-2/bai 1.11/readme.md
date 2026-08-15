# Bài 1.11 — Phân công n việc cho m người (thời gian khác nhau theo từng người)

## Đề bài

Có `n` công việc phân cho `m` người, mỗi việc giao đúng một người. Biết `t[i][j]` là thời gian **người i** làm **việc j**. Tìm phương án phân công sao cho thời gian hoàn thành tất cả công việc (tính từ lúc mọi người cùng bắt đầu) là nhỏ nhất.

Kiểm tra với `n = 8`, `m = 3`:

| | J1 | J2 | J3 | J4 | J5 | J6 | J7 | J8 |
|---|---|---|---|---|---|---|---|---|
| **Người 1** | 5 | 5 | 4 | 10 | 8 | 6 | 12 | 8 |
| **Người 2** | 7 | 5 | 7 | 3 | 9 | 7 | 8 | 5 |
| **Người 3** | 10 | 6 | 7 | 8 | 10 | 6 | 5 | 7 |

## Ý tưởng

Mọi người làm việc **song song**, nên thời gian hoàn thành cả nhóm chính là tổng thời gian của **người bận nhất**:

```
makespan(assign) = max( tổng t[i][j] của các việc j giao cho người i )
```

Đây là bài toán *unrelated parallel machines scheduling* (ký hiệu `R||Cmax`), thuộc lớp NP-hard, nên ta dùng heuristic 2 giai đoạn:

1. **Tham lam theo độ hối tiếc (regret)** — dựng nhanh một phương án tốt.
2. **Tìm kiếm cục bộ (hill climbing)** với hai phép biến đổi MOVE và SWAP — tinh chỉnh phương án đó.

Khác với bài 1.10 (các máy như nhau, chỉ cần cân bằng tổng thời gian), ở đây mỗi người **giỏi/dở khác nhau tùy việc**, nên phải cân nhắc cùng lúc hai yếu tố: *ai làm việc này nhanh* và *ai đang rảnh*.

## Cấu trúc dữ liệu

Một phương án phân công là mảng `assign` với `assign[j] = i` nghĩa là việc `j` giao cho người `i`.

```python
def tai_cua_nguoi(assign):
    # Tổng thời gian làm việc của từng người
    tai = [0] * m
    for j in range(n):
        tai[assign[j]] += t[assign[j]][j]
    return tai


def makespan(assign):
    # Thời gian hoàn thành = người bận nhất
    return max(tai_cua_nguoi(assign))


def danh_gia(assign):
    # So sánh theo thứ tự từ điển: ưu tiên makespan nhỏ, sau đó tổng thời gian nhỏ
    return (makespan(assign), tong_thoi_gian(assign))
```

`danh_gia` trả về **cặp** `(makespan, tổng công sức)`: hai phương án cùng makespan thì chọn phương án tốn ít công sức cả nhóm hơn. Tiêu chí phụ này vừa cho lời giải "gọn" hơn, vừa bảo đảm local search **luôn dừng** (cả hai giá trị đều giảm ngặt và bị chặn dưới).

## Giai đoạn 1 — Tham lam theo độ hối tiếc (regret)

Nếu duyệt việc theo thứ tự tùy ý thì những việc "kén người" (chỉ một người làm nhanh, người khác làm rất chậm) dễ bị xét sau cùng, lúc đó người phù hợp đã hết chỗ. Vì vậy ta xét trước việc có **regret** lớn:

```python
def do_hoi_tiec(j):
    # regret = (thời gian tốt nhì) - (thời gian tốt nhất) của việc j.
    # Regret lớn nghĩa là giao nhầm người sẽ thiệt nhiều -> phải xét sớm.
    cot = sorted(t[i][j] for i in range(m))
    return cot[1] - cot[0]


def tham_lam():
    assign = [-1] * n
    tai = [0] * m

    # Việc có regret lớn xét trước; bằng nhau thì việc "nặng" hơn xét trước
    thu_tu = sorted(range(n),
                    key=lambda j: (do_hoi_tiec(j), min(t[i][j] for i in range(m))),
                    reverse=True)

    for j in thu_tu:
        # Chọn người sao cho thời gian kết thúc của người đó sau khi nhận việc j là nhỏ nhất.
        # Bằng nhau thì ưu tiên người làm việc j nhanh hơn, rồi người đang rảnh hơn.
        i_tot = min(range(m), key=lambda i: (tai[i] + t[i][j], t[i][j], tai[i]))
        assign[j] = i_tot
        tai[i_tot] += t[i_tot][j]

    return assign
```

**Giải thích:** tiêu chí chọn người là `tai[i] + t[i][j]` — thời gian người `i` **kết thúc** nếu nhận thêm việc `j`. Công thức này tự động dung hòa: người làm nhanh nhưng đang quá tải sẽ thua người làm chậm hơn một chút mà đang rảnh.

## Giai đoạn 2 — Tìm kiếm cục bộ (hill climbing)

Coi mỗi phương án là một *trạng thái*; trạng thái lân cận là phương án chỉ khác một thao tác nhỏ:

```python
def all_neighbors(assign):
    neighbors = []

    # (i) MOVE: chuyển việc j sang người khác
    for j in range(n):
        for i in range(m):
            if i != assign[j]:
                hang_xom = copy.copy(assign)
                hang_xom[j] = i
                neighbors.append(hang_xom)

    # (ii) SWAP: đổi người phụ trách của hai việc j1, j2
    for j1 in range(n):
        for j2 in range(j1 + 1, n):
            if assign[j1] != assign[j2]:
                hang_xom = copy.copy(assign)
                hang_xom[j1], hang_xom[j2] = assign[j2], assign[j1]
                neighbors.append(hang_xom)

    return neighbors


def local_search(assign):
    while True:
        cai_thien = False
        diem_hien_tai = danh_gia(assign)

        for neighbor in all_neighbors(assign):
            # First-improvement: nhận ngay lân cận đầu tiên tốt hơn
            if danh_gia(neighbor) < diem_hien_tai:
                assign = neighbor
                cai_thien = True
                break

        # Duyệt hết lân cận mà không tốt hơn được nữa => cực tiểu cục bộ, dừng
        if not cai_thien:
            break

    return assign
```

Dùng **cả hai** phép biến đổi vì chúng bù cho nhau: chỉ *MOVE* thì hay bị kẹt khi cần đổi chéo hai việc, còn *SWAP* giữ nguyên số việc mỗi người nên tinh chỉnh được mà không làm lệch tải.

## Kiểm chứng

Chương trình tự đối chiếu kết quả heuristic với hai mốc:

```python
def can_duoi():
    # (1) Mỗi việc ít nhất tốn thời gian của người làm nhanh nhất, chia đều cho m người
    # (2) Việc "khó nhất" vẫn phải do một người làm trọn vẹn
    tong_min = sum(min(t[i][j] for i in range(m)) for j in range(n))
    viec_nang_nhat = max(min(t[i][j] for i in range(m)) for j in range(n))
    return max(-(-tong_min // m), viec_nang_nhat)
```

và **vét cạn** `m^n` phương án (chỉ chạy khi `m ** n <= 2_000_000`; với đề bài là `3^8 = 6561`, chạy tức thì).

## Kết quả với dữ liệu đề bài

```
Can duoi ly thuyet: 14

===== Giai doan 1: tham lam theo regret =====
Nguoi 1 | tong =  15 | J1(5), J3(4), J6(6)
Nguoi 2 | tong =  13 | J2(5), J4(3), J8(5)
Nguoi 3 | tong =  15 | J5(10), J7(5)
=> Makespan = 15 (tong cong suc = 43)

===== Giai doan 2: sau local search =====
Nguoi 1 | tong =  15 | J1(5), J3(4), J6(6)
Nguoi 2 | tong =  13 | J2(5), J4(3), J8(5)
Nguoi 3 | tong =  15 | J5(10), J7(5)
=> Makespan = 15 (tong cong suc = 43)

===== Kiem chung bang vet can (6561 phuong an) =====
Nguoi 1 | tong =  15 | J1(5), J3(4), J6(6)
Nguoi 2 | tong =  13 | J2(5), J4(3), J8(5)
Nguoi 3 | tong =  15 | J5(10), J7(5)
=> Makespan = 15 (tong cong suc = 43)
```

**Phương án phân công:**

| Người | Công việc | Thời gian | Tổng |
|---|---|---|---|
| Người 1 | J1, J3, J6 | 5 + 4 + 6 | **15** |
| Người 2 | J2, J4, J8 | 5 + 3 + 5 | **13** |
| Người 3 | J5, J7 | 10 + 5 | **15** |

**Thời gian hoàn thành tất cả công việc = 15.**

Vét cạn xác nhận 15 chính là **tối ưu** — riêng với bộ dữ liệu này thuật giải tham lam đã cho ngay lời giải tốt nhất nên local search không cải thiện thêm được. Cận dưới lý thuyết là 14 nhưng không đạt được (Người 3 buộc phải nhận J7 vì hai người kia làm việc đó quá chậm — 12 và 8).

## Minh họa vai trò của local search

Vì tham lam đã tối ưu sẵn ở bộ dữ liệu trên, chương trình chạy thêm một ví dụ xuất phát từ phương án **ngây thơ** — mỗi việc giao cho người làm nhanh nhất, bỏ qua chuyện cân bằng tải:

```
===== Minh hoa: khoi tao ngay tho =====
Nguoi 1 | tong =  28 | J1(5), J2(5), J3(4), J5(8), J6(6)
Nguoi 2 | tong =   8 | J4(3), J8(5)
Nguoi 3 | tong =   5 | J7(5)
=> Makespan = 28 (tong cong suc = 41)

===== Minh hoa: ngay tho + local search =====
Nguoi 1 | tong =  15 | J1(5), J3(4), J6(6)
Nguoi 2 | tong =  13 | J2(5), J4(3), J8(5)
Nguoi 3 | tong =  15 | J5(10), J7(5)
=> Makespan = 15 (tong cong suc = 43)
```

Local search kéo makespan từ **28 xuống 15**: nó chấp nhận cho Người 3 làm J5 mất 10 (thay vì Người 1 làm mất 8) để gỡ tải cho Người 1 — đúng tinh thần "tổng công sức tăng nhẹ nhưng thời gian hoàn thành giảm mạnh".

## Hướng dẫn sử dụng

Chỉ dùng thư viện chuẩn (`copy`, `itertools`), không cần cài thêm gói nào:

Chạy từ thư mục `week-2`:

```bash
python "bai 1.11/main.py"
```

Muốn chạy với dữ liệu khác, sửa ma trận `t` ở đầu `main.py` (mỗi hàng là một người, mỗi cột là một việc); `m` và `n` tự suy ra từ kích thước ma trận:

```python
t = [
    [5,  5, 4, 10,  8, 6, 12, 8],   # người 1
    [7,  5, 7,  3,  9, 7,  8, 5],   # người 2
    [10, 6, 7,  8, 10, 6,  5, 7],   # người 3
]
```

Lưu ý: phần vét cạn tự động bỏ qua khi `m ** n > 2.000.000` để không làm chậm chương trình với dữ liệu lớn.
