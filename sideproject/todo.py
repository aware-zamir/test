import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Database setup
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

# Add task
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

# Load tasks
def load_tasks():
    for row in task_table.get_children():
        task_table.delete(row)
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        status = "Completed" if task[2] else "Pending"
        task_table.insert("", tk.END, values=(task[1], status))

# Mark as completed
def complete_task():
    try:
        selected_item = task_table.selection()[0]
        task_id = task_table.item(selected_item)["values"][0]
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

# Delete task
def delete_task():
    try:
        selected_item = task_table.selection()[0]
        task_id = task_table.item(selected_item)["values"][0]
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

# GUI Setup
app = tk.Tk()
app.title("To-Do List")
app.geometry("600x450")  # Reduced size
app.configure(bg="#1E1E1E")  # Modern dark theme

# Title
title_label = tk.Label(
    app, 
    text="To-Do List", 
    font=("Arial", 18, "bold"), 
    bg="#1E1E1E", 
    fg="#FFFFFF"
)
title_label.pack(pady=10)

# Task Entry
task_entry = tk.Entry(
    app, 
    width=40,  # Reduced width
    font=("Arial", 12), 
    bg="#2D2D2D", 
    fg="#FFFFFF", 
    insertbackground="#FFFFFF"
)
task_entry.pack(pady=10)

# Task Table
columns = ("Task", "Status")
task_table = ttk.Treeview(app, columns=columns, show="headings", height=15)  # Reduced height
task_table.heading("Task", text="Task")
task_table.heading("Status", text="Status")
task_table.column("Task", width=400, anchor="w")
task_table.column("Status", width=100, anchor="center")
task_table.pack(pady=10)

# Style for Treeview
style = ttk.Style()
style.configure("Treeview", rowheight=25, font=("Arial", 10), background="#2D2D2D", foreground="#FFFFFF", fieldbackground="#2D2D2D")
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3C3C3C", foreground="#FFFFFF")
style.map("Treeview", background=[("selected", "#3C3C3C")], foreground=[("selected", "#FFFFFF")])

# Button Frame
button_frame = tk.Frame(app, bg="#1E1E1E")
button_frame.pack(pady=10)

# Buttons
tk.Button(
    button_frame, 
    text="Add", 
    command=add_task, 
    width=10, 
    bg="#4CAF50", 
    fg="#FFFFFF", 
    font=("Arial", 10)
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    button_frame, 
    text="Complete", 
    command=complete_task, 
    width=10, 
    bg="#2196F3", 
    fg="#FFFFFF", 
    font=("Arial", 10)
).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    button_frame, 
    text="Delete", 
    command=delete_task, 
    width=10, 
    bg="#F44336", 
    fg="#FFFFFF", 
    font=("Arial", 10)
).grid(row=0, column=2, padx=5, pady=5)

# Initialize Database and Load Tasks
setup_db()
load_tasks()
app.mainloop()
