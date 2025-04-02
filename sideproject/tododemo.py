import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Database setup remains the same
def setup_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Functions remain the same
def add_task():
    task = task_entry.get()
    if task:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, 0)", (task,))
        conn.commit()
        conn.close()
        task_entry.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def load_tasks():
    for item in task_table.get_children():
        task_table.delete(item)
    
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    
    for task in tasks:
        status = "✓" if task[2] else " "
        task_table.insert("", "end", values=(task[0], task[1], status), tags=('completed',) if task[2] else ())

def complete_task():
    try:
        selected_item = task_table.selection()[0]
        task_id = task_table.item(selected_item)['values'][0]
        
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task!")

def delete_task():
    try:
        selected_item = task_table.selection()[0]
        task_id = task_table.item(selected_item)['values'][0]
        
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task!")

# Enhanced GUI Setup
app = tk.Tk()
app.title("Task Manager")
app.geometry("800x600")
app.configure(bg="#f0f0f0")

# Style configuration
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#333333")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
style.configure("TEntry", padding=5)

# Main container
main_frame = tk.Frame(app, bg="#f0f0f0")
main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Header
header_frame = tk.Frame(main_frame, bg="#f0f0f0")
header_frame.pack(fill=tk.X, pady=(0, 20))

title_label = tk.Label(header_frame, text="Task Manager", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333333")
title_label.pack(side=tk.LEFT)

# Input frame
input_frame = tk.Frame(main_frame, bg="#f0f0f0")
input_frame.pack(fill=tk.X, pady=(0, 10))

task_entry = ttk.Entry(input_frame, font=("Arial", 12), width=50)
task_entry.pack(side=tk.LEFT, padx=(0, 10))

add_button = tk.Button(input_frame, text="Add Task", command=add_task, 
                      bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                      padx=15, pady=5, bd=0, cursor="hand2")
add_button.pack(side=tk.LEFT)

# Table
task_table = ttk.Treeview(main_frame, columns=("ID", "Task", "Status"), show="headings", height=15)
task_table.heading("ID", text="ID")
task_table.heading("Task", text="Task")
task_table.heading("Status", text="Status")

task_table.column("ID", width=50, anchor="center")
task_table.column("Task", width=600)
task_table.column("Status", width=100, anchor="center")

task_table.tag_configure('completed', foreground='#888888')
task_table.pack(fill=tk.BOTH, expand=True)

# Button frame
button_frame = tk.Frame(main_frame, bg="#f0f0f0")
button_frame.pack(pady=20)

complete_button = tk.Button(button_frame, text="Complete Task", command=complete_task,
                          bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                          padx=15, pady=5, bd=0, cursor="hand2")
complete_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Delete Task", command=delete_task,
                         bg="#F44336", fg="white", font=("Arial", 10, "bold"),
                         padx=15, pady=5, bd=0, cursor="hand2")
delete_button.pack(side=tk.LEFT, padx=5)

# Initialize
setup_db()
load_tasks()

# Center window on screen
window_width = 800
window_height = 600
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
app.geometry(f"{window_width}x{window_height}+{x}+{y}")

app.mainloop()
