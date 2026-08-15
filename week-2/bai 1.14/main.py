import copy

luan_van_tuple = [
    ("Q1", 205), ("Q2", 135), ("Q3", 80), ("Q4", 90),
    ("Q5", 70), ("Q6", 110), ("Q7", 60), ("Q8", 85),
    ("Q9", 200), ("Q10", 140), ("Q11", 170), ("Q12", 120),
]
luan_van_tuple.sort(key=lambda item: item[1], reverse=True)


def in_ket_qua(workers, tieu_de):
    print(f"\n===== {tieu_de} =====")
    for w in sorted(workers, key=lambda x: x["Name"]):
        speed = w.get("speed", 8)
        gio = w["pages"] / speed
        ds = ", ".join(w["jobs"])
        print(f'{w["Name"]:<8} | {w["pages"]:>4} trang | {gio:>5.2f} giờ | {ds}')

    ket_thuc = max(w["pages"] / w.get("speed", 8) for w in workers)
    print(f'{"":<8} | Thời gian hoàn thành (makespan): {ket_thuc:.2f} giờ')


def khoi_tao_lpt_cau_a():
    workers = [{"Name": f"W{i}", "jobs": [], "pages": 0} for i in range(1, 4)]
    for ten, so_trang in luan_van_tuple:
        worker = min(workers, key=lambda item: item["pages"])
        worker["jobs"].append(ten)
        worker["pages"] += so_trang
    return workers


def tim_phan_cong_toi_uu_cau_a():
    lpt = khoi_tao_lpt_cau_a()
    best_load = max(worker["pages"] for worker in lpt)
    best_jobs = [worker["jobs"][:] for worker in lpt]
    loads = [0, 0, 0]
    jobs = [[], [], []]

    def backtrack(index):
        nonlocal best_load, best_jobs
        if index == len(luan_van_tuple):
            current_load = max(loads)
            if current_load < best_load:
                best_load = current_load
                best_jobs = [assigned[:] for assigned in jobs]
            return

        ten, so_trang = luan_van_tuple[index]
        seen_loads = set()
        for worker_index in range(3):
            if loads[worker_index] in seen_loads:
                continue
            seen_loads.add(loads[worker_index])

            new_load = loads[worker_index] + so_trang
            if new_load >= best_load:
                continue

            loads[worker_index] = new_load
            jobs[worker_index].append(ten)
            backtrack(index + 1)
            jobs[worker_index].pop()
            loads[worker_index] -= so_trang

    backtrack(0)
    return [
        {"Name": f"W{i + 1}", "jobs": best_jobs[i], "pages": sum(dict(luan_van_tuple)[job] for job in best_jobs[i])}
        for i in range(3)
    ]


def makespan(workers):
    return max(worker["pages"] / worker["speed"] for worker in workers)


def all_neighbors(workers):
    neighbors = []
    trang = dict(luan_van_tuple)
    for a in range(len(workers)):
        for job in list(workers[a]["jobs"]):
            for b in range(len(workers)):
                if b != a:
                    new_workers = copy.deepcopy(workers)
                    new_workers[b]["jobs"].append(job)
                    new_workers[a]["jobs"].remove(job)
                    new_workers[a]["pages"] -= trang[job]
                    new_workers[b]["pages"] += trang[job]
                    neighbors.append(new_workers)

    for a in range(len(workers)):
        for job in workers[a]["jobs"]:
            for b in range(a + 1, len(workers)):
                for other_job in workers[b]["jobs"]:
                    new_workers = copy.deepcopy(workers)
                    new_workers[a]["jobs"].remove(job)
                    new_workers[a]["jobs"].append(other_job)
                    new_workers[b]["jobs"].remove(other_job)
                    new_workers[b]["jobs"].append(job)
                    new_workers[a]["pages"] += trang[other_job] - trang[job]
                    new_workers[b]["pages"] += trang[job] - trang[other_job]
                    neighbors.append(new_workers)
    return neighbors


def local_search(workers):
    while True:
        current_makespan = makespan(workers)
        for neighbor in all_neighbors(workers):
            if makespan(neighbor) < current_makespan:
                workers = neighbor
                break
        else:
            return workers


def main():
    in_ket_qua(tim_phan_cong_toi_uu_cau_a(), "Câu A (branch and bound, tối ưu)")

    workers = [
        {"Name": "W1", "speed": 8, "jobs": [], "pages": 0},
        {"Name": "W2", "speed": 8, "jobs": [], "pages": 0},
        {"Name": "W3", "speed": 8, "jobs": [], "pages": 0},
        {"Name": "Manager", "speed": 4, "jobs": [], "pages": 0},
    ]
    for ten, so_trang in luan_van_tuple:
        worker = min(workers, key=lambda item: (item["pages"] + so_trang) / item["speed"])
        worker["jobs"].append(ten)
        worker["pages"] += so_trang

    in_ket_qua(workers, "Câu B (khởi tạo tham lam)")
    in_ket_qua(local_search(workers), "Câu B (sau local search)")


if __name__ == "__main__":
    main()
