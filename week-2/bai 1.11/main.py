import copy
from itertools import product

# Bài 1.11: n công việc phân cho m người, t[i][j] = thời gian người i làm việc j.
# Mục tiêu: tối thiểu makespan = max tổng thời gian của một người.

# Dữ liệu đề bài: n = 8, m = 3
t = [
    [5,  5, 4, 10,  8, 6, 12, 8],   # người 1
    [7,  5, 7,  3,  9, 7,  8, 5],   # người 2
    [10, 6, 7,  8, 10, 6,  5, 7],   # người 3
]

m = len(t)
n = len(t[0])


def makespan(assign):
    # assign[j] = người được giao việc j -> makespan là tổng thời gian của người bận nhất
    return max(tai_cua_nguoi(assign))


def tai_cua_nguoi(assign):
    # Tổng thời gian làm việc của từng người
    tai = [0] * m
    for j in range(n):
        tai[assign[j]] += t[assign[j]][j]
    return tai


def tong_thoi_gian(assign):
    # Tổng công sức cả nhóm, chỉ dùng làm tiêu chí phụ khi makespan bằng nhau
    return sum(tai_cua_nguoi(assign))


def danh_gia(assign):
    # So sánh theo thứ tự từ điển: ưu tiên makespan nhỏ, sau đó tổng thời gian nhỏ
    return (makespan(assign), tong_thoi_gian(assign))


def in_ket_qua(assign, tieu_de):
    print(f"\n===== {tieu_de} =====")
    tai = tai_cua_nguoi(assign)
    for i in range(m):
        viec = [f"J{j + 1}({t[i][j]})" for j in range(n) if assign[j] == i]
        ds = ", ".join(viec) if viec else "(không có việc)"
        print(f"Nguoi {i + 1} | tong = {tai[i]:>3} | {ds}")
    print(f"=> Makespan = {makespan(assign)} (tong cong suc = {tong_thoi_gian(assign)})")


# Giai đoạn 1 — tham lam theo độ hối tiếc (regret)

def do_hoi_tiec(j):
    # regret = (thời gian tốt nhì) - (thời gian tốt nhất) của việc j.
    # Regret lớn nghĩa là giao nhầm người sẽ thiệt nhiều -> phải xét sớm.
    cot = sorted(t[i][j] for i in range(m))
    return cot[1] - cot[0]


def tham_lam():
    assign = [-1] * n
    tai = [0] * m

    # Việc có regret lớn xét trước; bằng nhau thì việc "nặng" hơn xét trước
    thu_tu = sorted(range(n), key=lambda j: (do_hoi_tiec(j), min(t[i][j] for i in range(m))), reverse=True)

    for j in thu_tu:
        # Chọn người sao cho thời gian kết thúc của người đó sau khi nhận việc j là nhỏ nhất.
        # Bằng nhau thì ưu tiên người làm việc j nhanh hơn, rồi người đang rảnh hơn.
        i_tot = min(range(m), key=lambda i: (tai[i] + t[i][j], t[i][j], tai[i]))
        assign[j] = i_tot
        tai[i_tot] += t[i_tot][j]

    return assign


# Giai đoạn 2 — tìm kiếm cục bộ (hill climbing) với MOVE và SWAP

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


# Kiểm chứng: cận dưới lý thuyết và vét cạn (chỉ chạy khi bài toán còn nhỏ)

def can_duoi():
    # (1) Mỗi việc ít nhất tốn thời gian của người làm nhanh nhất, chia đều cho m người
    # (2) Việc "khó nhất" vẫn phải do một người làm trọn vẹn
    tong_min = sum(min(t[i][j] for i in range(m)) for j in range(n))
    viec_nang_nhat = max(min(t[i][j] for i in range(m)) for j in range(n))
    return max(-(-tong_min // m), viec_nang_nhat)


def vet_can():
    tot_nhat = None
    for assign in product(range(m), repeat=n):
        assign = list(assign)
        if tot_nhat is None or danh_gia(assign) < danh_gia(tot_nhat):
            tot_nhat = assign
    return tot_nhat


print(f"Can duoi ly thuyet: {can_duoi()}")

greedy = tham_lam()
in_ket_qua(greedy, "Giai doan 1: tham lam theo regret")

ket_qua = local_search(greedy)
in_ket_qua(ket_qua, "Giai doan 2: sau local search")

if m ** n <= 2_000_000:
    in_ket_qua(vet_can(), f"Kiem chung bang vet can ({m ** n} phuong an)")

# Minh hoạ vai trò của local search: xuất phát từ một phương án ngây thơ
# (mỗi việc giao cho người làm nhanh nhất, bỏ qua chuyện cân bằng tải)
ngay_tho = [min(range(m), key=lambda i: t[i][j]) for j in range(n)]
in_ket_qua(ngay_tho, "Minh hoa: khoi tao ngay tho")
in_ket_qua(local_search(ngay_tho), "Minh hoa: ngay tho + local search")
