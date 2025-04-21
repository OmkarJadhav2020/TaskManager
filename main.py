#!/usr/bin/env python3
"""
TaskMaster CLI - A beautiful and feature-rich task tracking application
"""
import os
import sys
import time
import random
import argparse
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich import box
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.markdown import Markdown
from task_manager import TaskManager

# Initialize console for rich text rendering
console = Console()

# ASCII Art Banner
BANNER = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ████████╗ █████╗ ███████╗██╗  ██╗    ███╗   ███╗ █████╗ ███████╗████████╗║
║   ╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝    ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝║
║      ██║   ███████║███████╗█████╔╝     ██╔████╔██║███████║███████╗   ██║   ║
║      ██║   ██╔══██║╚════██║██╔═██╗     ██║╚██╔╝██║██╔══██║╚════██║   ██║   ║
║      ██║   ██║  ██║███████║██║  ██╗    ██║ ╚═╝ ██║██║  ██║███████║   ██║   ║
║      ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

MOTIVATIONAL_QUOTES = [
    "The secret of getting ahead is getting started. – Mark Twain",
    "It always seems impossible until it's done. – Nelson Mandela",
    "Don't watch the clock; do what it does. Keep going. – Sam Levenson",
    "The way to get started is to quit talking and begin doing. – Walt Disney",
    "You don't have to be great to start, but you have to start to be great. – Zig Ziglar",
    "Do the hard jobs first. The easy jobs will take care of themselves. – Dale Carnegie",
    "Focus on being productive instead of busy. – Tim Ferriss",
    "Until we can manage time, we can manage nothing else. – Peter Drucker",
    "The key is not to prioritize what's on your schedule, but to schedule your priorities. – Stephen Covey",
    "One of the great discoveries of man is the ability to arrange his time so that he can accomplish tasks. – Norman Vincent Peale"
]

# Initialize Task Manager
task_manager = TaskManager()

def display_banner():
    """Display colorful application banner"""
    console.print(Panel(Text(BANNER, style="bold cyan"), border_style="cyan", box=box.DOUBLE))
    quote = random.choice(MOTIVATIONAL_QUOTES)
    console.print(
        Panel(
            Align.center(Text(f"{quote}", style="italic yellow")),
            border_style="yellow",
            box=box.ROUNDED
        )
    )


def simulate_loading(message="Loading"):
    """Display a fancy loading spinner"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(f"[bold green]{message}...", total=100)
        for _ in range(10):
            progress.update(task, advance=10)
            time.sleep(0.1)

def add_task():
    """Add a new task with rich prompts and UI"""
    console.print("\n[bold cyan]✨ Creating a New Task ✨[/bold cyan]")
    
    title = Prompt.ask("[bold]Task title[/bold]")
    
    description = Prompt.ask("[bold]Description[/bold] (optional)", default="")
    
    has_due_date = Confirm.ask("[bold]Add a due date?[/bold]")
    due_date = None
    
    if has_due_date:
        console.print("[yellow]Due date options:[/yellow]")
        console.print("1. Today")
        console.print("2. Tomorrow")
        console.print("3. Next week")
        console.print("4. Custom date (YYYY-MM-DD)")
        
        date_choice = Prompt.ask("[bold]Choose an option[/bold]", choices=["1", "2", "3", "4"], default="1")
        
        today = datetime.now().date()
        if date_choice == "1":
            due_date = today.isoformat()
        elif date_choice == "2":
            due_date = (today + timedelta(days=1)).isoformat()
        elif date_choice == "3":
            due_date = (today + timedelta(days=7)).isoformat()
        elif date_choice == "4":
            while True:
                date_str = Prompt.ask("[bold]Enter date[/bold] (YYYY-MM-DD)")
                try:
                    # Validate the date format
                    parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    due_date = parsed_date.isoformat()
                    break
                except ValueError:
                    console.print("[bold red]Invalid date format! Please use YYYY-MM-DD.[/bold red]")
    
    priority = Prompt.ask(
        "[bold]Priority[/bold]", 
        choices=["low", "medium", "high"], 
        default="medium"
    )
    
    tags_input = Prompt.ask("[bold]Tags[/bold] (comma-separated, optional)", default="")
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
    
    simulate_loading("Adding task")
    
    task_id = task_manager.add_task(
        title=title, 
        description=description, 
        due_date=due_date, 
        priority=priority,
        tags=tags
    )
    
    console.print(f"\n[bold green]✅ Task added successfully with ID: {task_id}[/bold green]")

def list_tasks():
    """Display tasks in a beautiful table"""
    tasks = task_manager.get_tasks()
    
    # Show different views
    view_options = ["all", "pending", "completed", "priority", "due date"]
    console.print("\n[bold cyan]📋 Task List Views[/bold cyan]")
    for i, option in enumerate(view_options, 1):
        console.print(f"{i}. {option.title()}")
    
    view_choice = Prompt.ask("[bold]Choose a view[/bold]", choices=[str(i) for i in range(1, len(view_options) + 1)], default="1")
    view = view_options[int(view_choice) - 1]
    
    filtered_tasks = tasks
    
    # Filter tasks based on view
    if view == "pending":
        filtered_tasks = [task for task in tasks if not task["completed"]]
    elif view == "completed":
        filtered_tasks = [task for task in tasks if task["completed"]]
    
    # Sort tasks
    if view == "priority":
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        filtered_tasks = sorted(filtered_tasks, key=lambda x: priority_rank.get(x.get("priority", "medium"), 1))
    elif view == "due date":
        # Sort by due date, putting None values at the end
        filtered_tasks = sorted(
            filtered_tasks,
            key=lambda x: datetime.fromisoformat(x["due_date"]) if x.get("due_date") else datetime.max.date()
        )
    
    if not filtered_tasks:
        console.print("\n[bold yellow]No tasks found in this view![/bold yellow]")
        return
    
    simulate_loading("Fetching tasks")
    
    # Create a beautiful table
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    
    # Add columns to the table
    table.add_column("#", style="dim", width=6)
    table.add_column("Title", style="cyan", width=20)
    table.add_column("Description", style="green", width=30)
    table.add_column("Status", width=10)
    table.add_column("Due Date", width=12)
    table.add_column("Priority", width=10)
    table.add_column("Tags", width=15)
    
    # Add rows to the table
    for task in filtered_tasks:
        # Style status
        status_style = "green" if task["completed"] else "yellow"
        status = "✅ Done" if task["completed"] else "⏳ Pending"
        
        # Style due date
        due_date = task.get("due_date", "")
        if due_date:
            try:
                due_date_obj = datetime.fromisoformat(due_date)
                today = datetime.now().date()
                
                if due_date_obj.date() < today:
                    due_date_style = "bold red"
                    due_date_display = f"{due_date} ⚠️"
                elif due_date_obj.date() == today:
                    due_date_style = "bold yellow"
                    due_date_display = f"{due_date} 📅"
                else:
                    due_date_style = "blue"
                    due_date_display = due_date
            except (ValueError, TypeError):
                due_date_style = "blue"
                due_date_display = due_date
        else:
            due_date_style = "dim"
            due_date_display = "N/A"
        
        # Style priority
        priority = task.get("priority", "medium")
        priority_styles = {
            "high": "bold red",
            "medium": "bold yellow",
            "low": "green"
        }
        priority_style = priority_styles.get(priority, "yellow")
        
        # Format tags
        tags = ", ".join(task.get("tags", []))
        
        table.add_row(
            str(task["id"]),
            task["title"],
            (task["description"][:27] + "...") if len(task["description"]) > 30 else task["description"],
            f"[{status_style}]{status}[/{status_style}]",
            f"[{due_date_style}]{due_date_display}[/{due_date_style}]",
            f"[{priority_style}]{priority.upper()}[/{priority_style}]",
            tags
        )
    
    console.print("\n")
    console.print(table)
    
    # Display statistics
    total = len(tasks)
    completed = len([t for t in tasks if t["completed"]])
    pending = total - completed
    
    stats = Table.grid(padding=1)
    stats.add_column(style="green", justify="right")
    stats.add_column(style="cyan")
    
    stats.add_row("Total tasks:", str(total))
    stats.add_row("Completed:", str(completed))
    stats.add_row("Pending:", str(pending))
    stats.add_row(
        "Completion rate:", 
        f"[progress.percentage]{(completed/total)*100 if total else 0:.1f}%[/progress.percentage]"
    )
    
    console.print(Panel(stats, title="[bold]📊 Statistics[/bold]", border_style="blue"))

def mark_complete():
    """Mark a task as completed with nice UI effects"""
    task_id = Prompt.ask("\n[bold]Enter the ID of the task to mark as completed[/bold]")
    
    try:
        task_id = int(task_id)
    except ValueError:
        console.print("[bold red]❌ Error: Task ID must be a number[/bold red]")
        return
    
    task = task_manager.get_task_by_id(task_id)
    if not task:
        console.print(f"[bold red]❌ Error: No task found with ID {task_id}[/bold red]")
        return
    
    if task["completed"]:
        undo = Confirm.ask(f"[yellow]Task '{task['title']}' is already completed. Do you want to mark it as pending?[/yellow]")
        if undo:
            simulate_loading("Updating task")
            task_manager.toggle_task_status(task_id, False)
            console.print(f"[bold yellow]⟲ Task '{task['title']}' marked as pending[/bold yellow]")
        return
    
    simulate_loading("Updating task")
    task_manager.toggle_task_status(task_id)
    
    # Celebration animation
    console.print("\n[bold green]✅ Task completed! Great job![/bold green]")
    for _ in range(5):
        console.print(random.choice(["🎉", "🎊", "🥳", "👏", "⭐"]), end=" ")
    console.print("\n")

def delete_task():
    """Delete a task with confirmation"""
    task_id = Prompt.ask("\n[bold]Enter the ID of the task to delete[/bold]")
    
    try:
        task_id = int(task_id)
    except ValueError:
        console.print("[bold red]❌ Error: Task ID must be a number[/bold red]")
        return
    
    task = task_manager.get_task_by_id(task_id)
    if not task:
        console.print(f"[bold red]❌ Error: No task found with ID {task_id}[/bold red]")
        return
    
    confirm = Confirm.ask(
        f"[bold red]Are you sure you want to delete task '{task['title']}'?[/bold red] [dim]This cannot be undone[/dim]"
    )
    
    if confirm:
        simulate_loading("Deleting task")
        task_manager.delete_task(task_id)
        console.print(f"[bold green]🗑️ Task '{task['title']}' deleted successfully[/bold green]")
    else:
        console.print("[yellow]Deletion cancelled[/yellow]")

def search_tasks():
    """Search for tasks by keyword"""
    keyword = Prompt.ask("\n[bold]Enter search keyword[/bold]")
    
    simulate_loading("Searching tasks")
    
    tasks = task_manager.get_tasks()
    
    # Search in title, description, and tags
    results = []
    for task in tasks:
        if (keyword.lower() in task["title"].lower() or 
            keyword.lower() in task["description"].lower() or
            any(keyword.lower() in tag.lower() for tag in task.get("tags", []))):
            results.append(task)
    
    if not results:
        console.print(f"\n[yellow]No tasks found matching '{keyword}'[/yellow]")
        return
    
    # Create a beautiful table for search results
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    
    # Add columns to the table
    table.add_column("#", style="dim", width=6)
    table.add_column("Title", style="cyan", width=20)
    table.add_column("Description", style="green", width=30)
    table.add_column("Status", width=10)
    
    # Add rows to the table
    for task in results:
        status_style = "green" if task["completed"] else "yellow"
        status = "✅ Done" if task["completed"] else "⏳ Pending"
        
        table.add_row(
            str(task["id"]),
            task["title"],
            (task["description"][:27] + "...") if len(task["description"]) > 30 else task["description"],
            f"[{status_style}]{status}[/{status_style}]"
        )
    
    console.print("\n")
    console.print(Panel(
        table,
        title=f"[bold]🔍 Search Results for '{keyword}' ({len(results)} found)[/bold]",
        border_style="blue"
    ))

def view_task_details():
    """View detailed information about a specific task"""
    task_id = Prompt.ask("\n[bold]Enter the ID of the task to view[/bold]")
    
    try:
        task_id = int(task_id)
    except ValueError:
        console.print("[bold red]❌ Error: Task ID must be a number[/bold red]")
        return
    
    task = task_manager.get_task_by_id(task_id)
    if not task:
        console.print(f"[bold red]❌ Error: No task found with ID {task_id}[/bold red]")
        return
    
    simulate_loading("Loading task details")
    
    # Create a layout for task details
    layout = Layout()
    layout.split_column(
        Layout(name="header"),
        Layout(name="main"),
        Layout(name="footer")
    )
    
    # Header
    status = "✅ COMPLETED" if task["completed"] else "⏳ PENDING"
    status_style = "green" if task["completed"] else "yellow"
    header_text = Text(f"TASK #{task['id']}: {task['title']}", style="bold cyan")
    layout["header"].update(Panel(Align.center(header_text), style="cyan"))
    
    # Main content
    content = Table.grid(padding=1)
    content.add_column(style="bold", width=12)
    content.add_column()
    
    content.add_row("Status:", f"[{status_style}]{status}[/{status_style}]")
    
    # Format description with markdown
    description = task["description"] if task["description"] else "*No description provided*"
    content.add_row("Description:", description)
    
    # Format due date
    if task.get("due_date"):
        try:
            due_date_obj = datetime.fromisoformat(task["due_date"])
            today = datetime.now().date()
            
            if due_date_obj.date() < today:
                due_date_style = "bold red"
                due_date_display = f"{task['due_date']} (OVERDUE)"
            elif due_date_obj.date() == today:
                due_date_style = "bold yellow"
                due_date_display = f"{task['due_date']} (TODAY)"
            else:
                days_remaining = (due_date_obj.date() - today).days
                due_date_style = "blue"
                due_date_display = f"{task['due_date']} ({days_remaining} days remaining)"
        except (ValueError, TypeError):
            due_date_style = "blue"
            due_date_display = task["due_date"]
    else:
        due_date_style = "dim"
        due_date_display = "No due date set"
    
    content.add_row("Due Date:", f"[{due_date_style}]{due_date_display}[/{due_date_style}]")
    
    # Format priority
    priority = task.get("priority", "medium")
    priority_styles = {
        "high": "bold red",
        "medium": "bold yellow",
        "low": "green"
    }
    priority_style = priority_styles.get(priority, "yellow")
    content.add_row("Priority:", f"[{priority_style}]{priority.upper()}[/{priority_style}]")
    
    # Format tags
    tags = ", ".join(task.get("tags", [])) if task.get("tags") else "No tags"
    content.add_row("Tags:", tags)
    
    # Format created/updated dates
    created_at = datetime.fromisoformat(task.get("created_at", datetime.now().isoformat()))
    updated_at = datetime.fromisoformat(task.get("updated_at", datetime.now().isoformat()))
    
    content.add_row("Created:", created_at.strftime("%Y-%m-%d %H:%M:%S"))
    content.add_row("Updated:", updated_at.strftime("%Y-%m-%d %H:%M:%S"))
    
    layout["main"].update(Panel(content, title="[bold]📝 Task Details[/bold]", border_style="blue"))
    
    # Footer with actions
    footer_text = Text("Actions: [M]ark complete/pending | [E]dit | [D]elete | [B]ack to menu", style="dim")
    layout["footer"].update(Panel(Align.center(footer_text)))
    
    console.print(layout)
    
    # Handle actions
    action = Prompt.ask("[bold]Choose an action[/bold]", choices=["M", "E", "D", "B"], default="B")
    
    if action == "M":
        task_manager.toggle_task_status(task_id, not task["completed"])
        status_text = "pending" if task["completed"] else "completed"
        console.print(f"[bold green]✅ Task marked as {status_text}[/bold green]")
    elif action == "E":
        edit_task(task_id)
    elif action == "D":
        confirm = Confirm.ask(f"[bold red]Are you sure you want to delete this task?[/bold red]")
        if confirm:
            task_manager.delete_task(task_id)
            console.print(f"[bold green]🗑️ Task deleted successfully[/bold green]")
            return
    
    # Re-display task details if we didn't delete
    if action != "B" and action != "D":
        view_task_details()

def edit_task(task_id):
    """Edit an existing task"""
    task = task_manager.get_task_by_id(task_id)
    if not task:
        console.print(f"[bold red]❌ Error: No task found with ID {task_id}[/bold red]")
        return
    
    console.print(f"\n[bold cyan]✏️ Editing Task #{task_id}[/bold cyan]")
    
    # What field to edit
    console.print("What would you like to edit?")
    console.print("1. Title")
    console.print("2. Description")
    console.print("3. Due Date")
    console.print("4. Priority")
    console.print("5. Tags")
    console.print("6. All Fields")
    
    field_choice = Prompt.ask("[bold]Choose a field[/bold]", choices=["1", "2", "3", "4", "5", "6"], default="1")
    
    updated_task = task.copy()
    
    if field_choice in ["1", "6"]:
        updated_task["title"] = Prompt.ask("[bold]Title[/bold]", default=task["title"])
    
    if field_choice in ["2", "6"]:
        updated_task["description"] = Prompt.ask("[bold]Description[/bold]", default=task["description"])
    
    if field_choice in ["3", "6"]:
        has_due_date = Confirm.ask("[bold]Add a due date?[/bold]", default=bool(task.get("due_date")))
        
        if has_due_date:
            console.print("[yellow]Due date options:[/yellow]")
            console.print("1. Today")
            console.print("2. Tomorrow")
            console.print("3. Next week")
            console.print("4. Custom date (YYYY-MM-DD)")
            
            date_choice = Prompt.ask("[bold]Choose an option[/bold]", choices=["1", "2", "3", "4"], default="4")
            
            today = datetime.now().date()
            if date_choice == "1":
                updated_task["due_date"] = today.isoformat()
            elif date_choice == "2":
                updated_task["due_date"] = (today + timedelta(days=1)).isoformat()
            elif date_choice == "3":
                updated_task["due_date"] = (today + timedelta(days=7)).isoformat()
            elif date_choice == "4":
                default_date = task.get("due_date", "")
                while True:
                    date_str = Prompt.ask("[bold]Enter date[/bold] (YYYY-MM-DD)", default=default_date)
                    try:
                        # Validate the date format
                        parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        updated_task["due_date"] = parsed_date.isoformat()
                        break
                    except ValueError:
                        console.print("[bold red]Invalid date format! Please use YYYY-MM-DD.[/bold red]")
        else:
            # Remove due date if it exists
            if "due_date" in updated_task:
                updated_task.pop("due_date")
    
    if field_choice in ["4", "6"]:
        updated_task["priority"] = Prompt.ask(
            "[bold]Priority[/bold]", 
            choices=["low", "medium", "high"], 
            default=task.get("priority", "medium")
        )
    
    if field_choice in ["5", "6"]:
        current_tags = ", ".join(task.get("tags", []))
        tags_input = Prompt.ask("[bold]Tags[/bold] (comma-separated)", default=current_tags)
        updated_task["tags"] = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
    
    simulate_loading("Updating task")
    
    task_manager.update_task(task_id, updated_task)
    console.print(f"\n[bold green]✅ Task updated successfully![/bold green]")

def bulk_actions():
    """Perform actions on multiple tasks at once"""
    console.print("\n[bold cyan]🔄 Bulk Actions[/bold cyan]")
    
    console.print("1. Mark all tasks as completed")
    console.print("2. Mark all tasks as pending")
    console.print("3. Delete completed tasks")
    console.print("4. Delete all tasks")
    console.print("5. Delete tasks older than a specific date")
    
    action_choice = Prompt.ask("[bold]Choose an action[/bold]", choices=["1", "2", "3", "4", "5"], default="1")
    
    tasks = task_manager.get_tasks()
    affected_count = 0
    
    if action_choice == "1":
        # Mark all as completed
        for task in tasks:
            if not task["completed"]:
                task_manager.toggle_task_status(task["id"], True)
                affected_count += 1
        
        console.print(f"[bold green]✅ {affected_count} tasks marked as completed[/bold green]")
    
    elif action_choice == "2":
        # Mark all as pending
        for task in tasks:
            if task["completed"]:
                task_manager.toggle_task_status(task["id"], False)
                affected_count += 1
        
        console.print(f"[bold yellow]⟲ {affected_count} tasks marked as pending[/bold yellow]")
    
    elif action_choice == "3":
        # Delete completed tasks
        completed_tasks = [task for task in tasks if task["completed"]]
        
        if not completed_tasks:
            console.print("[yellow]No completed tasks to delete[/yellow]")
            return
        
        confirm = Confirm.ask(
            f"[bold red]Are you sure you want to delete all {len(completed_tasks)} completed tasks?[/bold red]"
        )
        
        if confirm:
            for task in completed_tasks:
                task_manager.delete_task(task["id"])
                affected_count += 1
            
            console.print(f"[bold green]🗑️ {affected_count} completed tasks deleted[/bold green]")
        else:
            console.print("[yellow]Deletion cancelled[/yellow]")
    
    elif action_choice == "4":
        # Delete all tasks
        if not tasks:
            console.print("[yellow]No tasks to delete[/yellow]")
            return
        
        confirm = Confirm.ask(
            f"[bold red]Are you sure you want to delete ALL {len(tasks)} tasks?[/bold red] [dim]This cannot be undone[/dim]"
        )
        
        if confirm:
            double_confirm = Confirm.ask(
                "[bold red]ARE YOU REALLY SURE? This will permanently erase all your tasks[/bold red]"
            )
            
            if double_confirm:
                for task in tasks:
                    task_manager.delete_task(task["id"])
                    affected_count += 1
                
                console.print(f"[bold green]🗑️ {affected_count} tasks deleted[/bold green]")
            else:
                console.print("[yellow]Deletion cancelled[/yellow]")
        else:
            console.print("[yellow]Deletion cancelled[/yellow]")
    
    elif action_choice == "5":
        # Delete tasks older than a specific date
        console.print("[yellow]Delete tasks created before:[/yellow]")
        console.print("1. Yesterday")
        console.print("2. Last week")
        console.print("3. Last month")
        console.print("4. Custom date (YYYY-MM-DD)")
        
        date_choice = Prompt.ask("[bold]Choose an option[/bold]", choices=["1", "2", "3", "4"], default="1")
        
        today = datetime.now().date()
        cutoff_date = None
        
        if date_choice == "1":
            cutoff_date = (today - timedelta(days=1))
        elif date_choice == "2":
            cutoff_date = (today - timedelta(weeks=1))
        elif date_choice == "3":
            cutoff_date = (today - timedelta(days=30))
        elif date_choice == "4":
            while True:
                date_str = Prompt.ask("[bold]Enter date[/bold] (YYYY-MM-DD)")
                try:
                    # Validate the date format
                    cutoff_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    break
                except ValueError:
                    console.print("[bold red]Invalid date format! Please use YYYY-MM-DD.[/bold red]")
        
        old_tasks = []
        for task in tasks:
            created_date = datetime.fromisoformat(task.get("created_at", "")).date()
            if created_date < cutoff_date:
                old_tasks.append(task)
        
        if not old_tasks:
            console.print(f"[yellow]No tasks found created before {cutoff_date.isoformat()}[/yellow]")
            return
        
        confirm = Confirm.ask(
            f"[bold red]Are you sure you want to delete {len(old_tasks)} tasks created before {cutoff_date.isoformat()}?[/bold red]"
        )
        
        if confirm:
            for task in old_tasks:
                task_manager.delete_task(task["id"])
                affected_count += 1
            
            console.print(f"[bold green]🗑️ {affected_count} old tasks deleted[/bold green]")
        else:
            console.print("[yellow]Deletion cancelled[/yellow]")

def export_tasks():
    """Export tasks to different formats"""
    console.print("\n[bold cyan]📤 Export Tasks[/bold cyan]")
    
    console.print("1. Export to CSV")
    console.print("2. Export to Markdown")
    console.print("3. Export to JSON")
    
    format_choice = Prompt.ask("[bold]Choose a format[/bold]", choices=["1", "2", "3"], default="1")
    
    # Which tasks to export
    console.print("\n[bold]Which tasks to export?[/bold]")
    console.print("1. All tasks")
    console.print("2. Pending tasks only")
    console.print("3. Completed tasks only")
    
    tasks_choice = Prompt.ask("[bold]Choose an option[/bold]", choices=["1", "2", "3"], default="1")
    
    tasks = task_manager.get_tasks()
    
    # Filter tasks based on choice
    if tasks_choice == "2":
        tasks = [task for task in tasks if not task["completed"]]
    elif tasks_choice == "3":
        tasks = [task for task in tasks if task["completed"]]
    
    if not tasks:
        console.print("[yellow]No tasks to export[/yellow]")
        return
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_choice == "1":
        # Export to CSV
        filename = f"tasks_export_{timestamp}.csv"
        
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['id', 'title', 'description', 'completed', 'due_date', 'priority', 'tags', 'created_at', 'updated_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for task in tasks:
                # Convert tags list to string
                task_copy = task.copy()
                task_copy['tags'] = ', '.join(task_copy.get('tags', []))
                writer.writerow(task_copy)
    
    elif format_choice == "2":
        # Export to Markdown
        filename = f"tasks_export_{timestamp}.md"
        
        with open(filename, 'w') as mdfile:
            mdfile.write("# Task List Export\n\n")
            mdfile.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for task in tasks:
                status = "✅ COMPLETED" if task["completed"] else "⏳ PENDING"
                mdfile.write(f"## [{task['id']}] {task['title']}\n\n")
                mdfile.write(f"**Status:** {status}\n\n")
                
                if task["description"]:
                    mdfile.write(f"**Description:** {task['description']}\n\n")
                
                if task.get("due_date"):
                    mdfile.write(f"**Due Date:** {task['due_date']}\n\n")
                
                if task.get("priority"):
                    mdfile.write(f"**Priority:** {task['priority'].upper()}\n\n")
                
                if task.get("tags"):
                    mdfile.write(f"**Tags:** {', '.join(task['tags'])}\n\n")
                
                mdfile.write(f"**Created:** {task.get('created_at', '')}\n\n")
                mdfile.write(f"**Updated:** {task.get('updated_at', '')}\n\n")
                mdfile.write("---\n\n")
    
    elif format_choice == "3":
        # Export to JSON
        filename = f"tasks_export_{timestamp}.json"
        
        import json
        
        with open(filename, 'w') as jsonfile:
            json.dump(tasks, jsonfile, indent=2)
    
    console.print(f"[bold green]✅ Tasks exported successfully to {filename}[/bold green]")

def show_help():
    """Display help information with rich formatting"""
    help_md = """
    # TaskMaster CLI Help

    ## Basic Commands
    
    * **add** - Add a new task
    * **list** - List all tasks
    * **complete** - Mark a task as completed
    * **delete** - Delete a task
    * **view** - View detailed information about a task
    * **search** - Search for tasks
    * **edit** - Edit an existing task
    * **bulk** - Perform actions on multiple tasks
    * **export** - Export tasks to different formats
    * **help** - Show this help menu
    * **exit** - Exit the application
    
    ## Tips & Tricks
    
    * Use the **search** command to find tasks by keyword
    * Use **tags** to categorize your tasks
    * Set **priorities** (low, medium, high) to organize your workflow
    * Use **due dates** to keep track of deadlines
    * Use **bulk** actions to manage multiple tasks at once
    * Export your tasks to share with others or keep backups
    
    ## Keyboard Shortcuts
    
    * Press **Ctrl+C** at any time to exit the application
    """
    
    console.print(Markdown(help_md))

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