from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional, Tuple

from .utils import safe_read_text_file


@dataclass
class CRDTOp:
    type: Literal["insert", "delete"]
    pos: int
    site_id: str
    value: Optional[str] = None
    length: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "pos": self.pos,
            "value": self.value,
            "length": self.length,
            "site_id": self.site_id,
        }

    @staticmethod
    def from_dict(data: dict) -> "CRDTOp":
        return CRDTOp(
            type=data["type"],
            pos=data["pos"],
            value=data.get("value"),
            length=data.get("length"),
            site_id=data["siteId"],
        )


class LSEQIdentifier:
    def __init__(self, pos: int, site_id: int, counter: int) -> None:
        self.pos: int = pos
        self.site_id: int = site_id
        self.counter: int = counter

    def __lt__(self, other: "LSEQIdentifier") -> bool:
        if self.pos != other.pos:
            return self.pos < other.pos
        if self.site_id != other.site_id:
            return self.site_id < other.site_id
        return self.counter < other.counter

    def __repr__(self) -> str:
        return f"LSEQId({self.pos},{self.site_id},{self.counter})"


class CRDTManager:
    def __init__(self, file_path: Optional[Path] = None) -> None:
        self.chars: List[Tuple[LSEQIdentifier, str]] = []
        self.site_id: int = 1  # TODO: assign unique site id per client
        self.counter: int = 0
        if file_path:
            content, success = safe_read_text_file(file_path)
            if success and content is not None:
                for i, c in enumerate(content):
                    self.chars.append((LSEQIdentifier(i, 0, i), c))
        # else: empty doc

    def get_content(self) -> str:
        return "".join(c for _, c in self.chars)

    def apply_operation(self, op: CRDTOp) -> None:
        if op.type == "insert":
            pos: int = op.pos
            value: str = op.value or ""
            for i, ch in enumerate(value):
                self.counter += 1
                lseq_id = LSEQIdentifier(pos + i, self.site_id, self.counter)
                self.chars.insert(pos + i, (lseq_id, ch))
        elif op.type == "delete":
            pos: int = op.pos
            length: int = op.length if op.length is not None else 1
            del self.chars[pos : pos + length]
        # TODO: Implement LSEQ logic for distributed/remote ops
