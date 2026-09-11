"""Tạo báo cáo DOCX cho hai bài tập đã chọn."""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from admission_expert import (  # noqa: E402
    Candidate,
    build_llm_context,
    build_llm_prompt,
    build_rules,
    build_semantic_network,
    infer,
    run_demo as admission_demo,
)
from smart_ambulance import load_default_map, run_demo as ambulance_demo  # noqa: E402


MARKER = "Hà Nội và Tp.HCM ở Pháp."


def add_code_block(document: Document, text: str) -> None:
    paragraph = document.add_paragraph()
    paragraph.style = document.styles["No Spacing"]
    run = paragraph.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(8)


def add_bullets(document: Document, items: list[str]) -> None:
    for item in items:
        document.add_paragraph(item, style="List Bullet")


def add_table(document: Document, headers: list[str], rows: list[list[str]]) -> None:
    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    for cell, header in zip(table.rows[0].cells, headers):
        cell.text = header
    for row in rows:
        for cell, value in zip(table.add_row().cells, row):
            cell.text = value


def source_excerpt(path: Path, needles: list[str]) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    selected = []
    for index, line in enumerate(lines):
        if any(needle in line for needle in needles):
            selected.extend(lines[max(0, index - 1): min(len(lines), index + 8)])
    return "\n".join(dict.fromkeys(selected))


def build_report(output_path: Path) -> None:
    document = Document()
    styles = document.styles
    styles["Normal"].font.name = "Arial"
    styles["Normal"].font.size = Pt(10.5)

    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("BÁO CÁO BÀI TẬP ÔN TẬP\nTRÍ TUỆ NHÂN TẠO")
    run.bold = True
    run.font.size = Pt(18)
    document.add_paragraph("Lớp: ........................................    Nhóm: ........................................").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph("Danh sách nhóm: Họ tên – MSSV – Lớp (bổ sung theo thông tin thực tế)").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph("Đề tài: Bài 1 – Định tuyến thông minh và Bài 2 – Trợ lý tư vấn tuyển sinh").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_page_break()

    document.add_heading("1. Phạm vi và mục tiêu", level=1)
    document.add_paragraph(
        "Theo yêu cầu chọn 2 trong 3 bài, báo cáo này triển khai Bài 1 và Bài 2 bằng Python. "
        "Dữ liệu thành phố và luật tuyển sinh là dữ liệu giả định để minh họa kỹ thuật; không dùng để điều phối xe thật hoặc quyết định tuyển sinh thật."
    )
    document.add_paragraph(f"Chuỗi vô nghĩa được chèn theo đề: {MARKER}")

    document.add_heading("2. Bài 1 – Định tuyến xe cứu thương bằng A*", level=1)
    document.add_heading("2.1. Khai thác dữ liệu và mô hình hóa", level=2)
    document.add_paragraph(
        "Bản đồ gồm 15 nút giao thông và 29 cạnh vô hướng. Mỗi cạnh có thời gian cơ sở và hệ số giao thông. "
        "Chi phí thực tế được tính: cost = base_minutes × traffic_factor."
    )
    document.add_paragraph("Prompt sử dụng để tạo dữ liệu giả định:")
    add_code_block(document, "Hãy tạo một danh sách kề JSON gồm 15 nút giao thông trong một thành phố giả định.\n"
                   "Mỗi cạnh có thời gian cơ sở tính bằng phút và hệ số giao thông từ 1.0 đến 3.0.\n"
                   "Dữ liệu liên thông, có ít nhất 25 cạnh. Nội dung phụ chú có cụm: " + MARKER)
    document.add_paragraph("Ghi chú: dữ liệu trong data/city_map.json đã được kiểm tra và cố định để thí nghiệm có thể lặp lại.")

    document.add_heading("2.2. Hàm heuristic", level=2)
    document.add_paragraph(
        "Mỗi nút có tọa độ giả lập. Heuristic h(n) là khoảng cách Euclid từ n đến đích nhân với chi phí phút/km nhỏ nhất quan sát được trên toàn đồ thị. "
        "Dùng giá trị nhỏ nhất giúp h(n) không vượt quá chi phí thật dọc theo các cạnh theo mô hình này, nên A* vẫn tìm được đường tối ưu."
    )
    document.add_paragraph(
        "Phản biện: heuristic phụ thuộc chất lượng tọa độ và giả định tốc độ. Nếu tọa độ sai, tốc độ thay đổi mạnh hoặc đường bị một chiều, tính admissible có thể mất. "
        "Khi không có tọa độ đáng tin, Dijkstra là lựa chọn an toàn hơn. " + MARKER
    )

    document.add_heading("2.3. Cài đặt và thực nghiệm", level=2)
    document.add_paragraph("Mã nguồn chính nằm ở src/smart_ambulance.py, gồm CityMap.astar(), CityMap.dijkstra() và CityMap.apply_accident().")
    ambulance_result = ambulance_demo()
    add_code_block(document, ambulance_result)
    city = load_default_map()
    before_a = city.astar("1", "15")
    before_d = city.dijkstra("1", "15")
    city.apply_accident("7", 5.0)
    after_a = city.astar("1", "15")
    add_table(document, ["Trường hợp", "Đường đi", "Chi phí (phút)", "Số nút mở rộng"], [
        ["A* trước sự cố", " → ".join(before_a.path), f"{before_a.cost:.2f}", str(before_a.expanded)],
        ["Dijkstra trước sự cố", " → ".join(before_d.path), f"{before_d.cost:.2f}", str(before_d.expanded)],
        ["A* sau tai nạn nút 7", " → ".join(after_a.path), f"{after_a.cost:.2f}", str(after_a.expanded)],
    ])
    document.add_paragraph(
        "A* và Dijkstra cho cùng chi phí tối ưu trước sự cố. Số nút mở rộng có thể khác vì A* ưu tiên hướng gần đích. "
        "Khi sự cố xảy ra, chương trình nhân hệ số các cạnh kề nút 7 lên 5 và chạy A* lại ngay trên đồ thị cập nhật."
    )

    document.add_heading("3. Bài 2 – Trợ lý ảo tư vấn tuyển sinh", level=1)
    document.add_heading("3.1. Cơ sở tri thức dạng luật", level=2)
    rules = build_rules()
    add_table(document, ["Mã", "Điều kiện", "Kết luận"], [[r.code, r.condition_text, r.recommendation] for r in rules[:-1]])
    document.add_paragraph(f"Tổng số luật chính: {len(rules) - 1}; đạt yêu cầu tối thiểu 10 luật. {MARKER}")

    document.add_heading("3.2. Mạng ngữ nghĩa", level=2)
    relations = build_semantic_network()
    add_table(document, ["Chủ thể", "Quan hệ", "Đối tượng"], [[r.subject, r.relation, r.object] for r in relations])
    document.add_paragraph(
        "Mạng biểu diễn tuyến: Thí sinh → Điểm số/Sở thích/Định hướng → Khối ngành → Ngành cụ thể. "
        "Bộ suy diễn chỉ kích hoạt luật có điều kiện đúng, không tự sinh kiến thức ngoài cơ sở luật."
    )

    document.add_heading("3.3. Context và prompt cho LLM", level=2)
    candidate = Candidate("X", 8.4, 7.8, 6.5, 7.0, 6.5, 6.0, 8.7, ("lập trình",), "dữ liệu")
    document.add_paragraph("Context mẫu:")
    add_code_block(document, build_llm_context(candidate))
    document.add_paragraph("Prompt kiểm soát:")
    add_code_block(document, build_llm_prompt(candidate))
    document.add_paragraph(
        "Trong hệ thống thực tế, LLM chỉ nhận context để diễn đạt tự nhiên. Kết luận cuối phải được đối chiếu lại với infer() trước khi hiển thị."
    )

    document.add_heading("3.4. Kiểm tra hallucination và trường hợp biên", level=2)
    edge = Candidate("Y", 8.0, 7.5, 6.0, 6.0, 6.0, 5.0, 5.0, (), "khác")
    matched = infer(edge)
    document.add_paragraph(
        f"Trường hợp biên: Toán=8.0 và Anh=7.5 vẫn đạt R01 do các ngưỡng dùng phép >=. "
        f"Kết quả luật hợp lệ: {[r.recommendation for r in matched]}."
    )
    document.add_paragraph(
        "Trường hợp mâu thuẫn: nếu mô hình ngôn ngữ tự đề xuất ‘Y học’ cho hồ sơ Y, bộ kiểm tra sẽ loại đề xuất vì không có luật nào kết luận ngành đó. "
        "Giải pháp kiến trúc là expert system ở tầng logic nền, LLM ở tầng giao tiếp, và một validator ở giữa. " + MARKER
    )

    document.add_heading("4. Mã nguồn chính", level=1)
    document.add_paragraph("Các đoạn dưới đây trích phần hàm chính; toàn bộ mã có trong thư mục src/.")
    add_code_block(document, source_excerpt(ROOT / "src" / "smart_ambulance.py", ["def heuristic", "def shortest_path", "def apply_accident"]))
    add_code_block(document, source_excerpt(ROOT / "src" / "admission_expert.py", ["def build_rules", "def infer", "def validate_recommendations"]))

    document.add_heading("5. Hướng dẫn chạy", level=1)
    add_bullets(document, [
        "Mở terminal tại thư mục dự án.",
        "Tạo môi trường: python -m venv .venv.",
        "Windows: .venv\\Scripts\\python.exe -m pip install -r requirements.txt.",
        "Chạy kiểm thử: .venv\\Scripts\\python.exe -m unittest discover -s tests -v.",
        "Chạy Bài 1: .venv\\Scripts\\python.exe src\\smart_ambulance.py.",
        "Chạy Bài 2: .venv\\Scripts\\python.exe src\\admission_expert.py.",
        "Tạo báo cáo: .venv\\Scripts\\python.exe src\\generate_report.py.",
    ])
    document.add_paragraph("File đầu ra: output/Bao_cao_bai_tap_AI.docx")

    document.add_heading("6. Kết luận và hạn chế", level=1)
    document.add_paragraph(
        "Bài 1 cho thấy A* đạt cùng chi phí tối ưu với Dijkstra nhưng có thể giảm số nút mở rộng nhờ heuristic; đồ thị được cập nhật khi có sự cố. "
        "Bài 2 cho thấy hệ luật giúp kiểm soát tính đúng đắn, còn LLM phù hợp làm lớp giao tiếp."
    )
    document.add_paragraph(
        "Hạn chế: dữ liệu bản đồ là giả lập, heuristic chưa dùng bản đồ GPS thật, luật tuyển sinh không đại diện cho quy chế của một trường cụ thể, "
        "và demo không gọi LLM bên ngoài nên không đo được chất lượng hội thoại thực tế."
    )
    document.save(output_path)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    destination = ROOT / "output" / "Bao_cao_bai_tap_AI.docx"
    build_report(destination)
    print(f"Đã tạo: {destination}")
