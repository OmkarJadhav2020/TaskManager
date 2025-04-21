
import time
import random
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from rich.text import Text
from rich.align import Align
from rich.markdown import Markdown
from context import console

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