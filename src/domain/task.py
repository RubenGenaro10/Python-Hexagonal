from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: Optional[str]
    title: str
    description: str
    completed: bool = False

    def mark_as_completed(self):
        self.completed = True
