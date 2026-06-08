from logger import log
from brain import call_ollama


def execute_task(task, task_type, plan):
    """
    根据任务类型生成更贴近真实交付物的结果
    """
    if task_type == "development":
        prompt = f"""
你是资深产品技术顾问。
请针对下面任务输出一份“开发交付草案”。

任务：
{task}

执行计划：
{chr(10).join(f"- {p}" for p in plan)}

请输出：
1. 需求说明
2. 功能模块
3. 数据设计建议
4. API/后端建议
5. 前端页面建议
6. 测试建议

使用中文，结构清晰。
"""
    elif task_type == "writing":
        prompt = f"""
你是专业内容策划。
请根据下面任务输出最终文案初稿。

任务：
{task}

执行计划：
{chr(10).join(f"- {p}" for p in plan)}

要求：
- 使用中文
- 贴近真实可用内容
- 如果是小红书文案，风格自然、有吸引力
"""
    elif task_type == "presentation":
        prompt = f"""
你是专业汇报顾问。
请根据下面任务输出一份 PPT 内容大纲初稿。

任务：
{task}

执行计划：
{chr(10).join(f"- {p}" for p in plan)}

请输出：
1. 封面标题
2. 汇报目录
3. 每页PPT的标题与要点
4. 结尾总结

使用中文，适合直接整理成PPT。
"""
    elif task_type == "research":
        prompt = f"""
你是研究助理。
请根据下面任务输出一份研究总结初稿。

任务：
{task}

执行计划：
{chr(10).join(f"- {p}" for p in plan)}

要求：
- 使用中文
- 结构清晰
- 包含问题、分析、结论、建议
"""
    elif task_type == "analysis":
        prompt = f"""
你是分析顾问。
请根据下面任务输出一份分析报告初稿。

任务：
{task}

执行计划：
{chr(10).join(f"- {p}" for p in plan)}

要求：
- 使用中文
- 结构清晰
- 包含现状、问题、原因、建议
"""
    else:
        prompt = f"""
请根据下面任务和计划，输出一份高质量结果草稿。

任务：
{task}

执行计划：
{chr(10).join(f"- {p}" for p in plan)}

要求：
- 使用中文
- 结构清晰
- 可直接阅读使用
"""

    try:
        log(f"Executor start: {task} | type={task_type}")
        result = call_ollama(prompt)
        if not result:
            return "未生成有效执行结果。"
        log(f"Executor success: {task}")
        return result
    except Exception as e:
        log(f"Executor error: {task} | {e}")
        return f"执行器生成失败：{e}"