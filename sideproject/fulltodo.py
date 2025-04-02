import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Functionality for the To-Do List App
def add_task():
    task = task_entry.get()
    if not task:  # Do nothing if the input is empty
        return
    task_listbox.insert(tk.END, task)
    task_entry.delete(0, tk.END)

def delete_task():
    selected_task_indices = task_listbox.curselection()
    for index in reversed(selected_task_indices):
        task_listbox.delete(index)

def clear_tasks():
    task_listbox.delete(0, tk.END)

def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    time_label.config(text=f" {current_time}")
    app.after(1000, update_time)

# Create the main application window
app = tk.Tk()
app.title("To-Do List")
app.geometry("300x400")
app.configure(bg="#2E2E2E")  # Dark background

# Input field
task_entry = tk.Entry(app, width=40, bg="#3E3E3E", fg="white", insertbackground="white")
task_entry.pack(pady=10)

# Frame for buttons
button_frame = tk.Frame(app, bg="#2E2E2E")
button_frame.pack(pady=5)

# Buttons
add_button = tk.Button(button_frame, text="Add Task", command=add_task, bg="#5E5E5E", fg="white")
add_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Delete Task", command=delete_task, bg="#5E5E5E", fg="white")
delete_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear All Tasks", command=clear_tasks, bg="#5E5E5E", fg="white")
clear_button.pack(side=tk.LEFT, padx=5)

# Listbox to display tasks
task_listbox = tk.Listbox(app, width=50, height=15, bg="#3E3E3E", fg="white", selectbackground="#5E5E5E", selectforeground="white")
task_listbox.pack(pady=10)

# Time label
time_label = tk.Label(app, text="", bg="#2E2E2E", fg="white", font=("Helvetica", 14))
time_label.pack(pady=5)

# Start updating time
update_time()

# Run the application
app.mainloop()
