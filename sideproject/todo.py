import tkinter as tk
from tkinter import messagebox
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
    task_list.delete(0, tk.END)
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        display_text = f"[✓] {task[1]}" if task[2] else f"[ ] {task[1]}"
        task_list.insert(tk.END, display_text)

# Mark as completed
def complete_task():
    try:
        selected_index = task_list.curselection()[0]
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks")
        task_ids = [row[0] for row in cursor.fetchall()]
        task_id = task_ids[selected_index]
        cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

# Delete task
def delete_task():
    try:
        selected_index = task_list.curselection()[0]
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks")
        task_ids = [row[0] for row in cursor.fetchall()]
        task_id = task_ids[selected_index]
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

# GUI Setup
app = tk.Tk()
app.title("To-Do List")
app.geometry("400x500")
app.configure(bg="#F0F0F0")

title_label = tk.Label(app, text="To-Do List", font=("Arial", 16, "bold"), bg="#F0F0F0")
title_label.pack(pady=10)

task_entry = tk.Entry(app, width=40)
task_entry.pack(pady=5)

task_list = tk.Listbox(app, width=50, height=15)
task_list.pack(pady=10)

button_frame = tk.Frame(app, bg="#F0F0F0")
button_frame.pack()

tk.Button(button_frame, text="Add", command=add_task, width=10, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Complete", command=complete_task, width=10, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Delete", command=delete_task, width=10, bg="#F44336", fg="white").grid(row=0, column=2, padx=5, pady=5)

setup_db()
load_tasks()
app.mainloop()
