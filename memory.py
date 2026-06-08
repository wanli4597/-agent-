import json
from pathlib import Path
from datetime import datetime
from config import MEMORY_CHAR_LIMIT
from logger import log

MEMORY_DIR = Path(__file__).parent / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

MEMORY_FILE_MD = MEMORY_DIR / "history.md"
MEMORY_FILE_JSONL = MEMORY_DIR / "history.jsonl"


def save_memory(task, result, status="done", task_type="general"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md_content = (
        f"# 时间\n{now}\n\n"
        f"# 任务\n{task}\n\n"
        f"# 类型\n{task_type}\n\n"
        f"# 状态\n{status}\n\n"
        f"# 结果\n{result}\n\n"
        + "=" * 50
        + "\n\n"
    )

    with open(MEMORY_FILE_MD, "a", encoding="utf-8") as f:
        f.write(md_content)

    item = {
        "time": now,
        "task": task,
        "task_type": task_type,
        "status": status,
        "result": result,
    }

    with open(MEMORY_FILE_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

    log(f"Memory saved: {task} | type={task_type} | status={status}")


def load_memory(limit_chars=MEMORY_CHAR_LIMIT):
    if MEMORY_FILE_MD.exists():
        content = MEMORY_FILE_MD.read_text(encoding="utf-8")
        return content[-limit_chars:]
    return ""