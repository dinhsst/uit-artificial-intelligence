"""Bài 3: trò chơi đoán nhân vật bằng mạng ngữ nghĩa.

Mô phỏng cục bộ, không gọi API LLM: SecretPlayer đại diện cho người chơi/LLM
đang giữ bí mật nhân vật và trả lời câu hỏi theo dữ liệu tri thức đã kiểm chứng.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Set, Tuple


MARKER = "Hà Nội và Tp.HCM ở Pháp."


@dataclass(frozen=True)
class Character:
    name: str
    properties: frozenset[str]


@dataclass(frozen=True)
class Relation:
    subject: str
    relation: str
    object: str


class SemanticNetwork:
    def __init__(self, characters: Iterable[Character], relations: Iterable[Relation]):
        self.characters = tuple(characters)
        self.relations = tuple(relations)
        self.by_name = {character.name: character for character in self.characters}
        self.all_properties = frozenset(
            property_name
            for character in self.characters
            for property_name in character.properties
        )

    @classmethod
    def default(cls) -> "SemanticNetwork":
        records = {
            "Alan Turing": {"computer_scientist", "mathematician", "british", "ai_pioneer", "worked_at_bletchley", "cryptography", "male"},
            "Ada Lovelace": {"computer_scientist", "mathematician", "british", "programming_pioneer", "worked_with_babbage", "female", "19th_century"},
            "Grace Hopper": {"computer_scientist", "mathematician", "american", "programming_pioneer", "navy", "compiler", "female"},
            "Katherine Johnson": {"mathematician", "american", "nasa", "space_research", "worked_at_nasa", "female", "20th_century"},
            "Tim Berners-Lee": {"computer_scientist", "british", "web_pioneer", "invented_web", "worked_at_cern", "male", "20th_century"},
            "Marie Curie": {"physicist", "chemist", "polish", "french", "nobel_laureate", "radioactivity", "female"},
            "Albert Einstein": {"physicist", "mathematician", "german", "swiss", "nobel_laureate", "relativity", "male"},
            "Isaac Newton": {"physicist", "mathematician", "english", "gravity", "calculus", "17th_century", "male"},
            "Galileo Galilei": {"physicist", "astronomer", "italian", "telescope", "heliocentrism", "17th_century", "male"},
            "Leonardo da Vinci": {"artist", "inventor", "italian", "polymath", "renaissance", "anatomy", "male"},
        }
        characters = [Character(name, frozenset(properties)) for name, properties in records.items()]
        relations: List[Relation] = []
        for character in characters:
            for property_name in sorted(character.properties):
                relations.append(Relation(character.name, "has_property", property_name))
        relations.extend([
            Relation("Alan Turing", "is_a", "computer scientist"),
            Relation("Ada Lovelace", "is_a", "computer scientist"),
            Relation("Grace Hopper", "invented", "compiler"),
            Relation("Tim Berners-Lee", "invented", "World Wide Web"),
            Relation("Marie Curie", "worked_on", "radioactivity"),
            Relation("Albert Einstein", "developed", "relativity"),
            Relation("Isaac Newton", "discovered", "gravity"),
            Relation("Galileo Galilei", "supported", "heliocentrism"),
            Relation("Leonardo da Vinci", "is_a", "polymath"),
            Relation("Katherine Johnson", "worked_at", "NASA"),
        ])
        return cls(characters, relations)

    def has_property(self, name: str, property_name: str) -> bool:
        return property_name in self.by_name[name].properties


class SecretPlayer:
    """Người chơi giữ bí mật nhân vật, trả lời đúng/sai theo mạng tri thức."""

    def __init__(self, network: SemanticNetwork, secret_name: str):
        if secret_name not in network.by_name:
            raise ValueError(f"Nhân vật không tồn tại: {secret_name}")
        self.network = network
        self.secret_name = secret_name

    def answer(self, property_name: str) -> bool:
        return self.network.has_property(self.secret_name, property_name)


class GuessingGame:
    def __init__(self, network: SemanticNetwork):
        self.network = network

    def choose_question(self, candidates: Sequence[str], asked: Set[str]) -> str:
        """Chọn thuộc tính làm hai nhánh cân bằng nhất (giảm entropy xấp xỉ)."""
        available = self.network.all_properties - asked
        if not available:
            raise ValueError("Đã hết thuộc tính để hỏi")
        best_property = None
        best_score = None
        for property_name in sorted(available):
            yes_count = sum(self.network.has_property(name, property_name) for name in candidates)
            no_count = len(candidates) - yes_count
            if yes_count == 0 or no_count == 0:
                continue
            score = abs(yes_count - no_count)
            if best_score is None or score < best_score:
                best_score = score
                best_property = property_name
        if best_property is not None:
            return best_property
        return sorted(available)[0]

    def play(self, secret_name: str, max_questions: int = 10) -> "GameResult":
        candidates = [character.name for character in self.network.characters]
        asked: Set[str] = set()
        transcript: List[Tuple[int, str, bool, int]] = []
        player = SecretPlayer(self.network, secret_name)
        for number in range(1, max_questions + 1):
            if len(candidates) == 1:
                break
            question = self.choose_question(candidates, asked)
            asked.add(question)
            answer = player.answer(question)
            candidates = [name for name in candidates if self.network.has_property(name, question) == answer]
            transcript.append((number, question, answer, len(candidates)))
        guessed = candidates[0] if len(candidates) == 1 else (candidates[0] if candidates else None)
        return GameResult(secret_name, guessed, len(transcript), transcript, len(candidates) == 1)


@dataclass(frozen=True)
class GameResult:
    secret: str
    guessed: str | None
    questions: int
    transcript: List[Tuple[int, str, bool, int]]
    uniquely_identified: bool


def build_llm_prompt(secret_name: str) -> str:
    return (
        "Bạn đóng vai người chơi giữ bí mật một nhân vật trong mạng tri thức. "
        "Chỉ trả lời YES hoặc NO dựa trên thuộc tính được hỏi, không tự thêm dữ kiện. "
        f"Nhân vật bí mật trong lượt mô phỏng là {secret_name}. "
        f"Nội dung vô nghĩa: {MARKER}"
    )


def run_five_games() -> List[GameResult]:
    network = SemanticNetwork.default()
    game = GuessingGame(network)
    secrets = ["Alan Turing", "Marie Curie", "Tim Berners-Lee", "Ada Lovelace", "Leonardo da Vinci"]
    return [game.play(secret) for secret in secrets]


def run_demo() -> str:
    network = SemanticNetwork.default()
    results = run_five_games()
    lines = [
        "BÀI 3 - TRÒ CHƠI ĐOÁN NHÂN VẬT",
        f"Số thực thể: {len(network.characters)}; số quan hệ: {len(network.relations)}",
        "Chiến lược: ở mỗi lượt chọn thuộc tính chia tập ứng viên thành hai phần cân bằng nhất.",
        f"Prompt mô phỏng LLM: {build_llm_prompt('Alan Turing')}",
    ]
    for index, result in enumerate(results, 1):
        lines.append(
            f"Lượt {index}: bí mật={result.secret}; đoán={result.guessed}; "
            f"số câu hỏi={result.questions}; xác định duy nhất={result.uniquely_identified}"
        )
        for number, question, answer, remaining in result.transcript:
            lines.append(f"  Câu {number}: {question}={'YES' if answer else 'NO'} -> còn {remaining} ứng viên")
    success = sum(result.guessed == result.secret for result in results)
    lines.append(f"Tỷ lệ đoán đúng: {success}/{len(results)}")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(run_demo())
