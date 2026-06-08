from collections import deque
from logger import log

task_queue = deque()


def add_task(task_item):
    task_queue.append(task_item)
    log(f"Task queued: {task_item['task']} | type={task_item.get('task_type', 'general')}")


def add_tasks(tasks, task_type="general", parent_task="", is_subtask=False):
    for t in tasks:
        add_task({
            "task": t,
            "status": "pending",
            "result": "",
            "error": "",
            "task_type": task_type,
            "parent_task": parent_task,
            "is_subtask": is_subtask,
        })


def get_next_task():
    if task_queue:
        return task_queue[0]
    return None


def start_task():
    if task_queue:
        task_queue[0]["status"] = "running"
        log(f"Task started: {task_queue[0]['task']}")


def complete_task(result=""):
    if task_queue:
        task = task_queue[0]
        task["status"] = "done"
        task["result"] = result
        log(f"Task completed: {task['task']}")
        return task_queue.popleft()
    return None


def fail_task(error=""):
    if task_queue:
        task = task_queue[0]
        task["status"] = "failed"
        task["error"] = str(error)
        log(f"Task failed: {task['task']} | {error}")
        return task_queue.popleft()
    return None


def has_tasks():
    return len(task_queue) > 0