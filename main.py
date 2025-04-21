"""
TaskMaster CLI - A beautiful and feature-rich task tracking application
"""
import os
import sys
import argparse
from rich.prompt import Prompt
from task_ui import display_banner,show_help
from task_commands import add_task,list_tasks,edit_task,mark_complete,delete_task,view_task_details,export_tasks,bulk_actions,search_tasks
from context import task_manager,console


def main():
    """Main function to run the CLI"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="TaskMaster CLI - A beautiful task tracking app")
    parser.add_argument("--add", action="store_true", help="Add a new task directly")
    parser.add_argument("--list", action="store_true", help="List all tasks directly")
    parser.add_argument("--complete", type=int, help="Mark a task as completed by ID")
    parser.add_argument("--delete", type=int, help="Delete a task by ID")
    
    args = parser.parse_args()
    
    # Process direct commands if provided
    if args.add:
        add_task()
        return
    elif args.list:
        list_tasks()
        return
    elif args.complete is not None:
        task_id = args.complete
        task = task_manager.get_task_by_id(task_id)
        if task:
            task_manager.toggle_task_status(task_id)
            console.print(f"[bold green]✅ Task #{task_id} marked as completed[/bold green]")
        else:
            console.print(f"[bold red]❌ Error: No task found with ID {task_id}[/bold red]")
        return
    elif args.delete is not None:
        task_id = args.delete
        task = task_manager.get_task_by_id(task_id)
        if task:
            task_manager.delete_task(task_id)
            console.print(f"[bold green]🗑️ Task #{task_id} deleted[/bold green]")
        else:
            console.print(f"[bold red]❌ Error: No task found with ID {task_id}[/bold red]")
        return
    
    # Interactive mode
    try:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        display_banner()
        
        while True:
            console.print("\n[bold cyan]📋 Main Menu[/bold cyan]")
            console.print("1. Add Task")
            console.print("2. List Tasks")
            console.print("3. Mark Task as Completed")
            console.print("4. Delete Task")
            console.print("5. View Task Details")
            console.print("6. Search Tasks")
            console.print("7. Edit Task")
            console.print("8. Bulk Actions")
            console.print("9. Export Tasks")
            console.print("H. Help")
            console.print("Q. Quit")
            
            choice = Prompt.ask(
                "\n[bold]Choose an option[/bold]", 
                choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "H", "Q", "h", "q"], 
                default="1"
            ).upper()
            
            if choice == "1":
                add_task()
            elif choice == "2":
                list_tasks()
            elif choice == "3":
                mark_complete()
            elif choice == "4":
                delete_task()
            elif choice == "5":
                view_task_details()
            elif choice == "6":
                search_tasks()
            elif choice == "7":
                task_id = Prompt.ask("\n[bold]Enter the ID of the task to edit[/bold]")
                try:
                    edit_task(int(task_id))
                except ValueError:
                    console.print("[bold red]❌ Error: Task ID must be a number[/bold red]")
            elif choice == "8":
                bulk_actions()
            elif choice == "9":
                export_tasks()
            elif choice == "H":
                show_help()
            elif choice == "Q":
                console.print("\n[bold green]👋 Thank you for using TaskMaster CLI! Have a productive day![/bold green]")
                break
    finally:

        task_manager.storage.save_tasks(task_manager.get_tasks())
        console.print("[bold green]💾 Tasks saved successfully before exit.[/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold green]👋 Thank you for using TaskMaster CLI! Have a productive day![/bold green]")
        sys.exit(0)