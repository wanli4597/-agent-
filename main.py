from config import APP_NAME, APP_LEVEL
from logger import log
from brain import think, classify_task
from planner import make_plan, should_expand
from executor import execute_task
from tools import save_markdown, save_text, save_report, safe_filename
from memory import save_memory
from task_queue import add_tasks, has_tasks, get_next_task, start_task, complete_task, fail_task

print("=" * 50)
print(f"🌟 {APP_NAME}")
print(f"Level   : {APP_LEVEL}")
print("Status  : Ready")
print("=" * 50)

task_counter = 1

while True:
    user_input = input("\n👨 老板（支持多个任务，用逗号分隔 / exit退出）：\n> ").strip()

    if user_input.lower() == "exit":
        print("\n✅ Nova：退出工作。")
        log("Application exited by user")
        break

    if not user_input:
        print("\n⚠️ 请输入至少一个任务。")
        continue

    root_tasks = [t.strip() for t in user_input.split(",") if t.strip()]

    for task in root_tasks:
        task_type = classify_task(task)
        add_tasks([task], task_type=task_type)

    print(f"\n📥 已加入任务队列：{len(root_tasks)} 个任务\n")

    while has_tasks():
        current = get_next_task()
        task = current["task"]
        task_type = current.get("task_type", "general")
        parent_task = current.get("parent_task", "")
        is_subtask = current.get("is_subtask", False)

        print("\n" + "=" * 50)
        print(f"🧠 正在执行任务：{task}")
        print(f"📌 类型：{task_type}")
        if is_subtask and parent_task:
            print(f"🔗 父任务：{parent_task}")
        print("=" * 50)

        start_task()
        base_name = f"task_{task_counter:03d}_{safe_filename(task)}"

        try:
            # Brain
            brain_result = think(task)

            print("\n🧠 思考结果：\n")
            if brain_result.success:
                print(brain_result.content)
            else:
                print(brain_result.error)

            # Planner
            plan = make_plan(task, task_type)
            print("\n📋 执行计划：")
            for i, step in enumerate(plan, 1):
                print(f"{i}. {step}")

            # Auto expand for large tasks
            if (not is_subtask) and should_expand(task, task_type):
                print("\n🪄 检测到这是一个较大的任务，已自动拆分为子任务并加入队列。")
                add_tasks(
                    plan,
                    task_type=task_type,
                    parent_task=task,
                    is_subtask=True
                )

            # Executor
            if brain_result.success:
                final_result = execute_task(task, task_type, plan)
                status = "done"
                error_text = ""
            else:
                final_result = "无有效执行结果"
                status = "failed"
                error_text = brain_result.error or "未知错误"

            # Save files
            content_for_md = brain_result.content if brain_result.success else error_text
            save_markdown(f"{base_name}.md", content_for_md)
            save_text(f"{base_name}_plan.txt", "\n".join(plan))
            save_text(f"{base_name}_result.txt", final_result)
            save_report(
                f"{base_name}_report.md",
                task=task,
                status=status,
                thinking=content_for_md,
                plan=plan,
                result=final_result,
                error=error_text
            )

            # Memory + queue
            if status == "done":
                save_memory(task, final_result, status="done", task_type=task_type)
                complete_task(result=final_result)
                print("\n✅ 任务完成\n")
            else:
                save_memory(task, error_text, status="failed", task_type=task_type)
                fail_task(error_text)
                print(f"\n❌ 任务失败：{error_text}\n")

        except Exception as e:
            fail_task(e)
            save_memory(task, f"任务执行失败：{e}", status="failed", task_type=task_type)
            print(f"\n❌ 任务失败：{e}\n")

        finally:
            task_counter += 1

    print("\n🎉 当前队列全部执行完成\n")