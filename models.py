from dataclasses import dataclass, field
from typing import List


@dataclass
class BrainResult:
    success: bool
    content: str
    error: str = ""


@dataclass
class TaskItem:
    task: str
    status: str = "pending"
    result: str = ""
    error: str = ""
    task_type: str = "general"
    parent_task: str = ""
    is_subtask: bool = False
    subtasks: List[str] = field(default_factory=list)