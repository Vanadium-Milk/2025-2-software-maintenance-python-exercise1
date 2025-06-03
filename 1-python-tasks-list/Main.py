import TaskManager

task_manager = TaskManager.TaskManager()

while True:

    print('''\nTASK MANAGER
            \r1. Add Task
            \r2. List Tasks
            \r3. Mark Task as Complete
            \r4. Delete Task
            \r5. Clear deleted log
            \r6. Exit''')

    choice = input("Enter your choice (1-5): ")
    
    if choice == "1":
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        task_manager.add_task(title, description)
    
    elif choice == "2":
        inc_del = input("Include deleted? y/n:")
        task_manager.list_tasks(inc_del == "Y" or inc_del == "y")
    
    elif choice == "3":
        task_id = int(input("Enter task ID to mark as complete: "))
        task_manager.mark_complete(task_id)
    
    elif choice == "4":
        task_id = int(input("Enter task ID to delete: "))
        task_manager.delete_task(task_id)
    
    elif choice == "5":
        task_manager.clear_flagged_tasks()

    elif choice == "6":
        print("Exiting Task Manager. Goodbye!")
        break
    
    else:
        print("Invalid choice. Please try again.")