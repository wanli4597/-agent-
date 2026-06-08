import re
from pathlib import Path
from config import MAX_FILENAME_LENGTH
from logger import log

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def safe_filename(text, max_length=MAX_FILENAME_LENGTH):
    text = text.strip().replace(" ", "_")
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    text = re.sub(r"_+", "_", text)
    return text[:max_length] if text else "task"


def save_markdown(filename, text):
    path = OUTPUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    log(f"Markdown saved: {path}")
    print(f"✅ 已保存Markdown文件：{path}")
    return path


def save_text(filename, text):
    path = OUTPUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    log(f"Text saved: {path}")
    print(f"✅ 已保存文本文件：{path}")
    return path


def save_report(filename, task, status, thinking, plan, result, error=""):
    path = OUTPUT_DIR / filename

    content = f"""# 任务报告

## 任务
{task}

## 状态
{status}

"""

    if error:
        content += f"""## 错误
{error}

"""

    content += f"""## 思考结果
{thinking}

## 执行计划
"""

    for i, step in enumerate(plan, 1):
        content += f"{i}. {step}\n"

    content += f"""
## 最终产出
{result}
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    log(f"Report saved: {path}")
    print(f"✅ 已保存任务报告：{path}")
    return path