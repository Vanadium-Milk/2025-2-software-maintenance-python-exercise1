import os
import json
from datetime import datetime

class TaskManager:
    '''
    Manage a json file with defined tasks.
    
    Implement basic crud functionality in tasks created by the user.
    Include names, description, status and creation date.
    '''
    
    __tasks: list[dict]
    __file_name: str

    def __init__(self):
        self.__tasks = []
        self.__file_name = "tasks.json"
        self.__load_tasks()
    

    def __load_tasks(self) -> None:
        if os.path.exists(self.__file_name):
            try:
                with open(self.__file_name, "r") as file:
                    self.__tasks = json.load(file)
            except:
                print("Error loading task data. Starting with empty task list.")
                self.__tasks = []
    

    def __save_tasks(self) -> None:
        with open(self.__file_name, "w") as file:
            json.dump(self.__tasks, file)
    
    
    def add_task(self, title: str, description: str) -> None:
        '''Create new task with the specified attributes'''

        task = {
            "id": len(self.__tasks) + 1,
            "title": title,
            "description": description,
            "status": "Pending",
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.__tasks.append(task)
        self.__save_tasks()
        print(f"Task '{title}' added successfully!")
    

    def list_tasks(self, include_deleted: bool = False) -> None:
        '''Print all the stored tasks, omit deleted unless specified'''

        if not self.__tasks:
            print("No tasks found.")
            return
        
        print("\n" + "=" * 80)
        print(f"{'ID':<5} {'TITLE':<20} {'STATUS':<10} {'CREATED DATE':<20} {'DESCRIPTION':<30}")
        print("-" * 80)
        
        current = []
        deleted = []
        for task in self.__tasks:
            row = f"{task['id']:<5} {task['title'][:18]:<20} {task['status']:<10} {task['created_date']:<20} {task['description'][:28]:<30}"
            
            if task["status"] != "Deleted":
                current.append(row)
            
            elif include_deleted:
                deleted.append(row)
        
        for i in current:
            print(i)
        
        if include_deleted:
            print("\nDeleted:")
            print("=" * 80)
            print("-" * 80)

            for i in deleted:
                print(i)

        print("=" * 80 + "\n")
    

    def mark_complete(self, task_id: int) -> None:
        '''Change the status of the specified task to \'Completed\''''

        for task in self.__tasks:
            if task["id"] == task_id:
                task["status"] = "Completed"
                self.__save_tasks()
                print(f"Task '{task['title']}' marked as completed!")
                return
        print(f"Task with ID {task_id} not found.")
    

    def delete_task(self, task_id: int) -> None:
        '''Flag the specified task for deletion, for permanent deletion use clear_flagged_tasks'''
        
        for task in self.__tasks:
            if task["id"] == task_id:
                task["status"] = "Deleted"
                self.__save_tasks()
                print(f"Task '{task['title']}' has been moved to the deleted log")
                return
        print(f"Task with ID {task_id} not found.")


    def clear_flagged_tasks(self) -> None:
        '''Permanently remove all the tasks from the deleted log'''

        cleared = 0
        for i, task in enumerate(self.__tasks):
            if task["status"] == "Deleted":
                self.__tasks.pop(i)
                cleared += 1

                print(f"Removed {cleared} tasks!")
                return
            
        self.__save_tasks()