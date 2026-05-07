from dataclasses import dataclass
from typing import Optional

@dataclass
class TranscriptionParams:
    file_path: str

@dataclass
class TranscriptionResult:
    text: str
    confidence: Optional[float] = None