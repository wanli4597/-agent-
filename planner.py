from config import MAX_SUBTASKS
from logger import log
from brain import call_ollama


def fallback_plan(task, task_type="general"):
    if task_type == "development":
        return [
            "梳理需求范围",
            "设计数据结构或数据库",
            "规划接口与模块",
            "编写核心功能方案",
            "制定测试与上线计划",
        ]

    if task_type == "writing":
        return [
            "明确主题和受众",
            "整理核心观点",
            "拟定内容结构",
            "输出初稿",
            "润色优化",
        ]

    if task_type == "presentation":
        return [
            "明确汇报目标",
            "整理资料",
            "设计PPT大纲",
            "撰写各页内容",
            "优化展示表达",
        ]

    if task_type == "research":
        return [
            "明确研究问题",
            "收集资料",
            "归纳重点信息",
            "形成结论",
            "输出研究总结",
        ]

    return [
        "理解任务目标",
        "拆分执行步骤",
        "准备所需资料",
        "开始产出结果",
    ]


def make_plan(task, task_type="general"):
    prompt = f"""
你是一个任务规划器。

任务：
{task}

任务类型：
{task_type}

请将任务拆成 4-6 个清晰、具体、可执行的步骤。
要求：
- 每行一个步骤
- 不要编号
- 使用中文
- 不要空泛
"""

    try:
        log(f"Planner start: {task}")
        content = call_ollama(prompt)
        lines = []

        for line in content.splitlines():
            line = line.strip().lstrip("-").lstrip("•").strip()
            if not line:
                continue
            if line[0].isdigit() and "." in line[:3]:
                line = line.split(".", 1)[1].strip()
            lines.append(line)

        lines = lines[:MAX_SUBTASKS]

        if len(lines) < 2:
            return fallback_plan(task, task_type)

        log(f"Planner success: {task}")
        return lines
    except Exception as e:
        log(f"Planner fallback: {task} | {e}")
        return fallback_plan(task, task_type)


def should_expand(task, task_type="general"):
    """
    判断是否需要拆成子任务：
    仅针对较大的开发/研究/分析/汇报任务
    """
    keywords = ["系统", "平台", "项目", "方案", "研究", "分析", "汇报", "PPT", "ppt"]
    if task_type in {"development", "research", "analysis", "presentation"}:
        return any(k.lower() in task.lower() for k in keywords) or len(task) >= 8
    return False