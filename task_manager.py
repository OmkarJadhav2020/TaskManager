#!/usr/bin/env python3
"""
Task Manager Module - Handles task operations like add, delete, complete, etc.
"""
import uuid
from datetime import datetime
from storage import Storage

class TaskManager:
    """Class to manage task operations"""
    
    def __init__(self):
        """Initialize the task manager with storage"""
        self.storage = Storage("tasks.json")
        self.tasks = self.storage.load_tasks()
    
    def get_tasks(self):
        """Get all tasks"""
        return self.tasks
    
    def get_task_by_id(self, task_id):
        """Get a task by its ID"""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def add_task(self, title, description="", due_date=None, priority="medium", tags=None):
        """
        Add a new task
        
        Args:
            title (str): Task title
            description (str, optional): Task description
            due_date (str, optional): Due date in ISO format
            priority (str, optional): Task priority (low, medium, high)
            tags (list, optional): List of tags
            
        Returns:
            int: The ID of the new task
        """
        # Generate a new task ID
        task_id = self._generate_task_id()
        
        # Create timestamp
        timestamp = datetime.now().isoformat()
        
        # Create new task
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "completed": False,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        # Add optional fields
        if due_date:
            task["due_date"] = due_date
        
        if priority:
            task["priority"] = priority
            
        if tags:
            task["tags"] = tags
        else:
            task["tags"] = []
        
        # Add task to list
        self.tasks.append(task)
        
        # Save tasks
        self.storage.save_tasks(self.tasks)
        
        return task_id
    
    def update_task(self, task_id, updated_task):
        """
        Update an existing task
        
        Args:
            task_id (int): ID of the task to update
            updated_task (dict): Dictionary containing updated task data
            
        Returns:
            bool: True if task was updated, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                # Keep the original ID and completion status
                updated_task["id"] = task_id
                
                # Update timestamp
                updated_task["updated_at"] = datetime.now().isoformat()
                
                # Keep creation timestamp
                updated_task["created_at"] = task.get("created_at", updated_task.get("created_at", datetime.now().isoformat()))
                
                # Update task
                self.tasks[i] = updated_task
                
                # Save tasks
                self.storage.save_tasks(self.tasks)
                
                return True
        
        return False
    
    def toggle_task_status(self, task_id, completed=True):
        """
        Toggle task completion status
        
        Args:
            task_id (int): ID of the task to toggle
            completed (bool, optional): New completion status
            
        Returns:
            bool: True if task was updated, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                # Update completion status
                self.tasks[i]["completed"] = completed
                
                # Update timestamp
                self.tasks[i]["updated_at"] = datetime.now().isoformat()
                
                # Save tasks
                self.storage.save_tasks(self.tasks)
                
                return True
        
        return False
    
    def delete_task(self, task_id):
        """
        Delete a task
        
        Args:
            task_id (int): ID of the task to delete
            
        Returns:
            bool: True if task was deleted, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                # Delete task
                del self.tasks[i]
                
                # Save tasks
                self.storage.save_tasks(self.tasks)
                
                return True
        
        return False
    
    def _generate_task_id(self):
        """Generate a unique task ID"""
        if not self.tasks:
            return 1
        
        # Find the highest ID
        max_id = max(task["id"] for task in self.tasks)
        
        # Return the next ID
        return max_id + 1