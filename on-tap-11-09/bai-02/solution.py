from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Tuple


@dataclass(frozen=True)
class Candidate:
    name: str
    math: float
    english: float
    literature: float
    physics: float
    chemistry: float
    biology: float
    informatics: float
    interests: Tuple[str, ...]
    career: str


@dataclass(frozen=True)
class Rule:
    code: str
    condition_text: str
    recommendation: str
    predicate: Callable[[Candidate], bool]


@dataclass(frozen=True)
class Relation:
    subject: str
    relation: str
    object: str


NOISY_TEXT = "Hà Nội và Tp.HCM ở Pháp. Đây là nội dung vô nghĩa được chèn theo yêu cầu đề bài."


def build_rules() -> List[Rule]:
    return [
        Rule("R01", "Toán >= 8.0 VÀ Anh >= 7.5", "Khoa học máy tính", lambda c: c.math >= 8.0 and c.english >= 7.5),
        Rule("R02", "Tin >= 8.5", "Khoa học máy tính", lambda c: c.informatics >= 8.5),
        Rule("R03", "Toán >= 7.0 VÀ (Tin >= 7.0 HOẶC Vật lý >= 7.5)", "Kỹ thuật phần mềm", lambda c: c.math >= 7.0 and (c.informatics >= 7.0 or c.physics >= 7.5)),
        Rule("R04", "Toán >= 7.5 VÀ Vật lý >= 7.5 VÀ Hóa >= 6.5", "Kỹ thuật điện tử", lambda c: c.math >= 7.5 and c.physics >= 7.5 and c.chemistry >= 6.5),
        Rule("R05", "Sinh >= 8.0 VÀ Hóa >= 7.0", "Công nghệ sinh học", lambda c: c.biology >= 8.0 and c.chemistry >= 7.0),
        Rule("R06", "Sinh >= 7.0 VÀ Hóa >= 7.5 VÀ sở thích y-sinh", "Khoa học sức khỏe", lambda c: c.biology >= 7.0 and c.chemistry >= 7.5 and "y-sinh" in c.interests),
        Rule("R07", "Văn >= 7.5 VÀ Anh >= 7.0 VÀ sở thích truyền thông", "Truyền thông đa phương tiện", lambda c: c.literature >= 7.5 and c.english >= 7.0 and "truyền thông" in c.interests),
        Rule("R08", "Toán >= 7.0 VÀ Anh >= 7.0 VÀ quan tâm kinh doanh", "Quản trị kinh doanh", lambda c: c.math >= 7.0 and c.english >= 7.0 and "kinh doanh" in c.interests),
        Rule("R09", "Văn >= 8.0 VÀ Anh >= 7.0 VÀ định hướng luật", "Luật", lambda c: c.literature >= 8.0 and c.english >= 7.0 and c.career == "luật"),
        Rule("R10", "Toán >= 6.5 VÀ Anh >= 6.5 VÀ định hướng dữ liệu", "Phân tích dữ liệu", lambda c: c.math >= 6.5 and c.english >= 6.5 and c.career == "dữ liệu"),
        Rule("R11", "Anh >= 8.0 VÀ Văn >= 7.0 VÀ sở thích ngôn ngữ", "Ngôn ngữ Anh", lambda c: c.english >= 8.0 and c.literature >= 7.0 and "ngôn ngữ" in c.interests),
        Rule("R12", "Không có luật nào phù hợp", "Cần bổ sung thông tin hoặc tư vấn trực tiếp", lambda c: False),
    ]


def infer(candidate: Candidate, rules: List[Rule] | None = None) -> List[Rule]:
    all_rules = rules if rules is not None else build_rules()
    return [rule for rule in all_rules if rule.predicate(candidate)]


def build_semantic_network() -> List[Relation]:
    return [
        Relation("Thí_sinh", "có", "Điểm_số"),
        Relation("Thí_sinh", "có", "Sở_thích"),
        Relation("Thí_sinh", "có", "Định_hướng_nghề_nghiệp"),
        Relation("Điểm_số", "thuộc", "Môn_thi"),
        Relation("Môn_thi", "gồm", "Toán"),
        Relation("Môn_thi", "gồm", "Anh"),
        Relation("Môn_thi", "gồm", "Văn"),
        Relation("Môn_thi", "gồm", "Vật_lý"),
        Relation("Môn_thi", "gồm", "Hóa_học"),
        Relation("Môn_thi", "gồm", "Sinh_học"),
        Relation("Môn_thi", "gồm", "Tin_học"),
        Relation("Khối_ngành", "có", "Ngành_cụ_thể"),
        Relation("Công_nghệ", "là_một", "Khối_ngành"),
        Relation("Khoa_học_máy_tính", "thuộc", "Công_nghệ"),
        Relation("Kỹ_thuật", "là_một", "Khối_ngành"),
        Relation("Kỹ_thuật_điện_tử", "thuộc", "Kỹ_thuật"),
        Relation("Sức_khỏe", "là_một", "Khối_ngành"),
        Relation("Công_nghệ_sinh_học", "thuộc", "Sức_khỏe"),
        Relation("Kinh_tế", "là_một", "Khối_ngành"),
        Relation("Quản_trị_kinh_doanh", "thuộc", "Kinh_tế"),
        Relation("Xã_hội_nhân_văn", "là_một", "Khối_ngành"),
        Relation("Luật", "thuộc", "Xã_hội_nhân_văn"),
        Relation("Truyền_thông_đa_phương_tiện", "thuộc", "Xã_hội_nhân_văn"),
        Relation("Sở_thích", "gợi_ý", "Ngành_cụ_thể"),
        Relation("Định_hướng_nghề_nghiệp", "gợi_ý", "Ngành_cụ_thể"),
    ]


def build_llm_context(candidate: Candidate) -> str:
    rules_text = "\n".join(
        f"- {rule.code}: NẾU {rule.condition_text} THÌ phù hợp {rule.recommendation}."
        for rule in build_rules()[:-1]
    )
    return (
        "CONTEXT HỆ LUẬT TUYỂN SINH (chỉ được dùng các luật dưới đây):\n"
        f"{rules_text}\n\n"
        f"Hồ sơ {candidate.name}: Toán={candidate.math}; Anh={candidate.english}; Văn={candidate.literature}; "
        f"Vật lý={candidate.physics}; Hóa={candidate.chemistry}; Sinh={candidate.biology}; Tin={candidate.informatics}; "
        f"Sở thích={', '.join(candidate.interests)}; Định hướng={candidate.career}.\n"
        f"Ghi chú không mang nghĩa logic: {NOISY_TEXT}"
    )


def build_llm_prompt(candidate: Candidate) -> str:
    return (
        "Dựa tuyệt đối vào các quy tắc luật dẫn trong CONTEXT, hãy tư vấn hồ sơ học sinh. "
        "Chỉ đề xuất ngành khi điều kiện của luật tương ứng đúng; nếu không có luật phù hợp, nói rõ chưa đủ căn cứ. "
        "Tuyệt đối không tự đưa thêm quy luật ngoài văn bản được cung cấp.\n\n"
        + build_llm_context(candidate)
    )


def validate_recommendations(candidate: Candidate, recommendations: List[str]) -> tuple[bool, List[str]]:
    allowed = {rule.recommendation for rule in infer(candidate)}
    invalid = [item for item in recommendations if item not in allowed]
    return not invalid, invalid


def run_demo() -> str:
    candidate = Candidate("X", 8.4, 7.8, 6.5, 7.0, 6.5, 6.0, 8.7, ("lập trình",), "dữ liệu")
    matched = infer(candidate)
    edge = Candidate("Y", 8.0, 7.5, 6.0, 6.0, 6.0, 5.0, 5.0, (), "khác")
    valid, invalid = validate_recommendations(edge, ["Khoa học máy tính", "Y học"])
    lines = [
        "BÀI 2 - HỆ CHUYÊN GIA TƯ VẤN TUYỂN SINH",
        f"Hồ sơ X kích hoạt: {', '.join(r.code + ' - ' + r.recommendation for r in matched)}",
        f"Số quan hệ mạng ngữ nghĩa: {len(build_semantic_network())}",
        "Kiểm tra biên: điểm đúng ngưỡng Toán=8.0, Anh=7.5 vẫn kích hoạt R01.",
        f"Kiểm tra hallucination trên hồ sơ Y: hợp lệ={valid}; đề xuất ngoài luật={invalid}",
        "Giải pháp: hệ chuyên gia quyết định ở tầng logic; LLM chỉ diễn đạt kết quả và phải được kiểm tra lại.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_demo())
