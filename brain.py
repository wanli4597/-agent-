import requests
from memory import load_memory
from config import OLLAMA_URL, MODEL, REQUEST_TIMEOUT, OLLAMA_API_KEY
from logger import log
from models import BrainResult


def call_ollama(prompt):
    headers = {}
    if OLLAMA_API_KEY:
        headers["X-API-Key"] = OLLAMA_API_KEY

    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        headers=headers or None,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    result = response.json()
    return result.get("response", "").strip()


def think(task):
    history = load_memory()

    prompt = f"""
你是 Nova AI Agent。
你是一名专业、务实、简洁的 AI 助理。

下面是历史任务记录（仅供参考）：
{history}

--------------------------------
老板的新任务：
{task}

请输出：
1. 任务理解
2. 任务类型判断
3. 关键缺失信息
4. 建议下一步动作

要求：
- 使用中文
- 条理清晰
- 不要空话
"""

    try:
        log(f"Brain start: {task}")
        content = call_ollama(prompt)
        if not content:
            return BrainResult(success=False, content="", error="Nova 未返回有效结果。")
        log(f"Brain success: {task}")
        return BrainResult(success=True, content=content)
    except Exception as e:
        log(f"Brain error: {task} | {e}")
        return BrainResult(success=False, content="", error=f"调用 Ollama 失败：{e}")


def classify_task(task):
    prompt = f"""
请判断下面任务属于哪一类，只输出一个英文标签：

任务：
{task}

可选标签：
development
writing
presentation
research
analysis
general
"""

    try:
        result = call_ollama(prompt).lower().strip()
        allowed = {"development", "writing", "presentation", "research", "analysis", "general"}
        return result if result in allowed else "general"
    except Exception:
        task_lower = task.lower()
        if "开发" in task or "系统" in task or "api" in task_lower:
            return "development"
        if "文案" in task or "写作" in task or "小红书" in task:
            return "writing"
        if "ppt" in task_lower or "汇报" in task:
            return "presentation"
        if "研究" in task or "调研" in task:
            return "research"
        if "分析" in task:
            return "analysis"
        return "general"