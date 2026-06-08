# Nova Final Edition (Local Agent)

Nova 是一个本地可运行的 Python CLI Agent，面向日常任务处理场景。

## 功能

- 本地 Ollama 调用（无需云端 API）
- 任务分类（development / writing / presentation / research / analysis / general）
- 任务规划（4-6 步）
- 按任务类型执行并产出结果
- 队列处理（支持批量任务）
- 大任务自动拆分子任务并继续入队
- 结果落盘（Markdown / txt / report）
- 历史记忆持久化（`memory/history.md` + `memory/history.jsonl`）
- 运行日志（`logs/nova.log`）

## 环境要求

- Python 3.9+
- 已安装并启动 Ollama（默认地址：`http://localhost:11434`）

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 可选环境变量

- `OLLAMA_URL`（默认：`http://localhost:11434/api/generate`）
- `OLLAMA_MODEL`（默认：`qwen2.5:7b`）
- `REQUEST_TIMEOUT`（默认：`180`，秒）
- `OLLAMA_API_KEY`（可选，默认空）

> 使用本地 Ollama 时通常不需要 API Key。
