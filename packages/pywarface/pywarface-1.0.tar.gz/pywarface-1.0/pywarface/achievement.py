from dataclasses import dataclass


@dataclass
class Achievement:
    """Metadata for achievements"""

    name: str
    progress: int
    completion_time: str
