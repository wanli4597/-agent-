# Nova Final Edition Local Agent

本项目提供一个可本地运行的 Nova CLI Agent，基于 Ollama 调用本地大模型，支持任务分类、规划、执行、队列处理、记忆持久化、日志记录和结果产出。

## 项目结构

- `config.py`：全局配置（模型、超时、限制）
- `logger.py`：日志写入
- `models.py`：结果与任务数据模型
- `memory.py`：历史记忆持久化（`memory/history.md` + `memory/history.jsonl`）
- `tools.py`：安全文件名与输出产物保存
- `brain.py`：任务理解与分类（Ollama）
- `planner.py`：任务规划与大任务自动扩展判定
- `executor.py`：按任务类型执行生成结果
- `task_queue.py`：任务队列处理
- `main.py`：CLI 主入口

## 环境要求

- Python 3.10+
- 本地运行中的 Ollama（默认 `http://localhost:11434`）
- 可用模型（默认 `qwen2.5:7b`）

## 安装

```bash
cd /tmp/workspace/wanli4597/-agent-
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 运行

```bash
python3 main.py
```

输入示例：

```text
开发库存管理系统, 写一篇小红书文案, 做一个项目汇报PPT
```

退出命令：`exit`

## 运行产物

- `output/`：每个任务的思考、计划、执行结果与汇总报告
- `memory/history.md` 与 `memory/history.jsonl`：记忆历史
- `logs/nova.log`：运行日志
