from datetime import datetime
from psycopg2.extras import RealDictCursor

from db import get_connection


class TaskManager:
    def __init__(self):
        self.conn = get_connection()

    def add_task(self, title: str, description: str) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (title, description, status, created_date)
                VALUES (%s, %s, %s, %s)
                """,
                (title, description, "Pending", datetime.now())
            )
            print(f"Task '{title}' added successfully!")

    def list_tasks(self, include_deleted: bool = False) -> None:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            if include_deleted:
                cur.execute("SELECT * FROM tasks ORDER BY id")
            else:
                cur.execute("SELECT * FROM tasks WHERE status != 'Deleted' ORDER BY id")
            tasks = cur.fetchall()

            if not tasks:
                print("No tasks found.")
                return
            
            print("\n" + "=" * 80)
            print(f"{'ID':<5} {'TITLE':<20} {'STATUS':<10} {'CREATED DATE':<20} {'DESCRIPTION':<30}")
            print("-" * 80)

            for task in tasks:
                row = f"{task['id']:<5} {task['title'][:18]:<20} {task['status']:<10} {task['created_date'].strftime('%Y-%m-%d %H:%M:%S'):<20} {task['description'][:28]:<30}"
                print(row)

            print("=" * 80 + "\n")

    def mark_complete(self, task_id: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET status = 'Completed'
                WHERE id = %s
                """,
                (task_id,)
            )
            if cur.rowcount > 0:
                print(f"Task ID {task_id} marked as completed!")
            else:
                print(f"Task with ID {task_id} not found.")

    def delete_task(self, task_id: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET status = 'Deleted'
                WHERE id = %s
                """,
                (task_id,)
            )
            if cur.rowcount > 0:
                print(f"Task ID {task_id} has been moved to the deleted log")
            else:
                print(f"Task with ID {task_id} not found.")

    def clear_flagged_tasks(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM tasks
                WHERE status = 'Deleted'
                """
            )
            print(f"Deleted {cur.rowcount} tasks permanently.")
