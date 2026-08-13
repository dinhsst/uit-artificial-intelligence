import copy

luan_van_tuple = [
    ("Q1", 205), ("Q2", 135), ("Q3", 80), ("Q4", 90),
    ("Q5", 70), ("Q6", 110), ("Q7", 60), ("Q8", 85),
    ("Q9", 200), ("Q10", 140), ("Q11", 170), ("Q12", 120)
]

# Sắp xếp giảm dần theo số trang
luan_van_tuple.sort(key=lambda item: item[1], reverse=True)

# Cái này em dùng để trình bày đẹp đẹp thui hehe
def in_ket_qua(workers, tieu_de):
    print(f"\n===== {tieu_de} =====")
    for w in sorted(workers, key=lambda x: x["Name"]):
        speed = w.get("speed", 8)          
        gio = w["pages"] / speed
        ds = ", ".join(w["jobs"])
        print(f'{w["Name"]:<8} | {w["pages"]:>4} trang | {gio:>5.1f} giờ | {ds}')

    makespan = max(w["pages"] / w.get("speed", 8) for w in workers)
    print(f'{"":<8} | Thời gian hoàn thành (makespan): {makespan:.2f} giờ')

# Câu A

workers = [{"Name": "W1", "jobs": [], "pages": 0}, {"Name": "W2", "jobs": [], "pages": 0}, {"Name": "W3", "jobs": [], "pages": 0}]

for luan_van in luan_van_tuple:
    workers.sort(key=lambda item: item["pages"])
    min_worker = workers[0]
    min_worker["jobs"].append(luan_van[0])
    min_worker["pages"] += luan_van[1]

tong_thoi_gian = max(workers, key=lambda w: w["pages"])["pages"] / 8

in_ket_qua(workers, "Câu A")

# Câu B

workers = [{"Name": "W1","speed": 8, "jobs": [], "pages": 0}, 
           {"Name": "W2","speed": 8, "jobs": [], "pages": 0}, 
           {"Name": "W3","speed": 8, "jobs": [], "pages": 0},
           {"Name": "Manager","speed": 4, "jobs": [], "pages": 0},]

for luan_van in luan_van_tuple:
    workers.sort(key=lambda item: (item["pages"] + luan_van[1]) / item["speed"])
    min_worker = workers[0]
    min_worker["jobs"].append(luan_van[0])
    min_worker["pages"] += luan_van[1]

tong_thoi_gian = max(workers, key=lambda w: w["pages"] / w["speed"])["pages"] / max(workers, key=lambda w: w["pages"] / w["speed"])["speed"]

in_ket_qua(workers, "Câu B (no local search)")

# Cải tiến kết quả bằng local search
def makespan(workers):
    return max(w["pages"] / w["speed"] for w in workers)

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
            if makespan(neighbor) < makespan_hien_tai:
                workers = neighbor
                cai_thien = True
                break
        
        if not cai_thien:
            break
    
    return workers

in_ket_qua(local_search(workers), "Câu B (with local search)")
