#!/usr/bin/env python3
"""
Storage Module - Handles reading and writing task data to JSON file
"""
import os
import json
from datetime import datetime

class Storage:
    """Class to manage task storage operations"""
    
    def __init__(self, filename):
        """
        Initialize the storage with a filename
        
        Args:
            filename (str): JSON file to store tasks
        """
        self.filename = filename
    
    def load_tasks(self):
        """
        Load tasks from JSON file
        
        Returns:
            list: List of tasks
        """
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, 'r') as file:
                tasks = json.load(file)
                
                # Handle backwards compatibility with older versions
                for task in tasks:
                    # Ensure all tasks have an ID
                    if "id" not in task:
                        task["id"] = hash(task["title"] + datetime.now().isoformat())
                    
                    # Ensure all tasks have timestamps
                    if "created_at" not in task:
                        task["created_at"] = datetime.now().isoformat()
                    
                    if "updated_at" not in task:
                        task["updated_at"] = datetime.now().isoformat()
                    
                    # Ensure all tasks have a tags field
                    if "tags" not in task:
                        task["tags"] = []
                
                return tasks
        except (json.JSONDecodeError, FileNotFoundError):
            # If the file is empty or invalid, return an empty list
            return []
    
    def save_tasks(self, tasks):
        """
        Save tasks to JSON file
        
        Args:
            tasks (list): List of tasks to save
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            
            # Write tasks to file
            with open(self.filename, 'w') as file:
                json.dump(tasks, file, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def backup_tasks(self):
        """
        Create a backup of the current tasks file
        
        Returns:
            str: Backup filename or None if backup failed
        """
        if not os.path.exists(self.filename):
            return None
        
        try:
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{os.path.splitext(self.filename)[0]}_backup_{timestamp}.json"
            
            # Read current file
            with open(self.filename, 'r') as source:
                data = source.read()
            
            # Write to backup file
            with open(backup_filename, 'w') as target:
                target.write(data)
            
            return backup_filename
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None