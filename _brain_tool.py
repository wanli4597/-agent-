import requests
from pathlib import Path

# Ollama本地API
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

# 输出文件夹
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def think(task):
    """Brain思考任务"""
    prompt = f"""
你是一名AI Agent。
任务：{task}

请生成：
1. Markdown文档内容（标记为 <MD>...</MD>）
2. Python代码骨架（标记为 <PY>...</PY>）
只输出文本，不要说明。
"""
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False}
    )
    result = response.json()
    return result["response"]

def save_files(text):
    """提取标记并生成对应文件"""
    md_content = ""
    py_content = ""
    # 提取 <MD>...</MD> 和 <PY>...</PY>
    import re
    md_match = re.search(r"<MD>(.*?)</MD>", text, re.DOTALL)
    py_match = re.search(r"<PY>(.*?)</PY>", text, re.DOTALL)
    if md_match:
        md_content = md_match.group(1).strip()
        with open(OUTPUT_DIR / "today.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"✅ 已保存Markdown文件：{OUTPUT_DIR / 'today.md'}")
    if py_match:
        py_content = py_match.group(1).strip()
        with open(OUTPUT_DIR / "today.py", "w", encoding="utf-8") as f:
            f.write(py_content)
        print(f"✅ 已保存Python文件：{OUTPUT_DIR / 'today.py'}")
    return md_content, py_content