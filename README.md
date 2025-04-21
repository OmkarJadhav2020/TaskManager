
# TaskMaster CLI

A beautiful, feature-rich task tracking application for the command line.

## 🌟 Features

- **Colorful and Interactive UI** using Rich library for Python  
- **Task Management**
  - Add, view, edit, and delete tasks  
  - Mark tasks as complete/pending  
  - Set priorities (low, medium, high)  
  - Add due dates  
  - Tag tasks for better organization  
- **Advanced Features**
  - Search tasks by keywords  
  - Bulk actions (complete all, delete completed, etc.)  
  - Export tasks to CSV, Markdown, or JSON  
  - Detailed task view with status indicators  
  - Sort tasks by priority or due date  
- **User Experience**
  - Beautiful ASCII art banner  
  - Loading animations  
  - Motivational quotes  
  - Interactive prompts  
  - Complete help system  

## 📋 Requirements

- Python 3.6+
- Rich library (`pip install rich`)

## 📦 Setup

1. Download all the project files and open the project folder.

2. Install dependencies:

```bash
pip install rich
```

3. Make the main script executable (optional, for Unix/Linux/Mac):

```bash
chmod +x main.py
```

## 🚀 Usage

### Interactive Mode

Run the application without any arguments to enter interactive mode:

```bash
python main.py
```

This will display the main menu where you can:
- Add new tasks  
- List existing tasks  
- Mark tasks as completed  
- Delete tasks  
- View task details  
- Search tasks  
- Edit tasks  
- Perform bulk actions  
- Export tasks  
- View help information  

### Command Line Arguments

You can also use TaskMaster directly from the command line:

```bash
# Add a new task (opens add dialog)
python main.py --add

# List all tasks
python main.py --list

# Mark a task as completed
python main.py --complete <task_id>

# Delete a task
python main.py --delete <task_id>
```

## 🧩 Project Structure

```
task_tracker/
│
├── main.py              # CLI entry point and user interface  
├── task_manager.py      # Task management logic (add, delete, etc.)  
├── storage.py           # Data persistence (JSON file handling)  
├── tasks.json           # Data storage file (auto-created)  
└── README.md            # This documentation  
```

## 🎨 Color Scheme and UI

TaskMaster CLI uses a carefully designed color scheme to make task management pleasant:

- **Cyan**: Headers, banners, and titles  
- **Green**: Success messages and completed tasks  
- **Yellow**: Pending tasks, warnings, and in-progress indicators  
- **Red**: Errors, high priority tasks, and overdue dates  
- **Magenta**: Table headers  
- **Blue**: Information panels and due dates  

## 📊 Task Properties

Each task in TaskMaster can have the following properties:

- **ID**: Unique identifier for the task  
- **Title**: Short description of the task  
- **Description**: Detailed information about the task (optional)  
- **Status**: Pending or completed  
- **Due Date**: Deadline for the task (optional)  
- **Priority**: Low, medium, or high  
- **Tags**: Keywords to categorize the task (optional)  
- **Created At**: When the task was created  
- **Updated At**: When the task was last modified  

## 💡 Tips and Tricks

- Use **tags** to organize related tasks  
- Set **priorities** to focus on what's important  
- Use the **search** function to quickly find tasks  
- Export your tasks regularly as a backup  
- Use **bulk actions** to manage multiple tasks at once  
- Check your task list daily to stay organized  

## 🛠️ Development Process and Challenges

During the development of TaskMaster CLI, I faced several challenges:

1. **Creating an Intuitive UI**: Making a command-line application user-friendly required careful planning of the menu structure and interaction flow.  
2. **Color Coordination**: Balancing aesthetics with readability when using colors in the terminal.  
3. **Data Persistence**: Ensuring tasks are properly saved and loaded, with error handling for file operations.  
4. **Feature Selection**: Deciding which features would be most useful without overcomplicating the application.  
5. **Code Organization**: Structuring the code into modules that are both maintainable and extendable.  

I overcame these challenges by:  
- Leveraging the Rich library for beautiful terminal rendering  
- Using a modular design with clear separation of concerns  
- Implementing comprehensive error handling  
- Testing with different usage scenarios  

## 🔮 Future Enhancements

Some features I'd like to add in future versions:

- **Task Categories**: Organize tasks into projects or categories  
- **Recurring Tasks**: Set tasks to repeat daily, weekly, monthly  
- **Task Dependencies**: Make tasks dependent on the completion of others  
- **Collaborative Features**: Share tasks between users  
- **Data Synchronization**: Sync tasks with cloud services  
- **Time Tracking**: Track how long you spend on each task  
- **User Accounts**: Multi-user support with authentication  
- **Task Templates**: Create templates for repetitive tasks  

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Rich](https://github.com/Textualize/rich) library for beautiful terminal formatting  
- Icons and ASCII art from various open sources  

## 👤 Author

Created with ❤️ by [Omkar Jadhav]

---

Thank you for using TaskMaster CLI! I hope it helps you stay organized and productive. If you have any questions or suggestions, please feel free to reach out to me.

Happy task managing! 🚀
