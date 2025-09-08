
from typing import List

class TaskManager:
    

    def __init__(self):
        
        self.tasks: List[str] = []

    def add_task(self, task: str) -> None:
        
        if not task:
            raise ValueError("Task cannot be empty")
        self.tasks.append(task)
        print(f"Task added: {task}")

    def remove_task(self, task: str) -> None:
       
        if task in self.tasks:
            self.tasks.remove(task)
            print(f"Task removed: {task}")
        else:
            print("Task not found.")
