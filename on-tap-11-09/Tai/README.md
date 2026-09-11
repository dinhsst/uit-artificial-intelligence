# Bài tập ôn tập Trí tuệ nhân tạo

Bộ bài làm chọn **Bài 1** và **Bài 2** theo đề trong `BAITAP.txt`.

## Nội dung

- `src/smart_ambulance.py`: bản đồ giả định, A*, Dijkstra và cập nhật sự cố.
- `src/admission_expert.py`: 12 luật IF-THEN, mạng ngữ nghĩa và validator chống hallucination.
- `src/generate_report.py`: tạo báo cáo `output/Bao_cao_bai_tap_AI.docx`.
- `data/city_map.json`: 15 nút và 29 cạnh dữ liệu giả lập.
- `tests/test_solutions.py`: kiểm thử tự động.

## Chạy bằng `.venv` trên Windows

```text
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\python.exe src\smart_ambulance.py
.venv\Scripts\python.exe src\admission_expert.py
.venv\Scripts\python.exe src\generate_report.py
```

Báo cáo được tạo tại `output/Bao_cao_bai_tap_AI.docx`. Các thông tin lớp, nhóm và danh sách thành viên đang để trống để điền theo thực tế.
