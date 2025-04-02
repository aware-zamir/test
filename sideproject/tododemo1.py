import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Theme colors
DARK_BG = "#1a1a1a"
DARKER_BG = "#141414"
TEXT_COLOR = "#e0e0e0"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List")
        self.root.geometry("800x600")
        self.root.configure(bg=DARK_BG)
        
        self.setup_database()
        self.setup_gui()
        self.load_tasks()
        
    def setup_database(self):
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                priority TEXT DEFAULT 'Medium',
                due_date TEXT
            )
        """)
        self.conn.commit()

    def setup_gui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background=DARKER_BG, foreground=TEXT_COLOR, rowheight=30)

        # Create treeview
        self.tree = ttk.Treeview(self.root, columns=("ID", "Task", "Status", "Priority", "Due Date"), show="headings")
        
        # Set column widths
        widths = [50, 300, 100, 100, 150]
        for col, width in zip(self.tree["columns"], widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        buttons = [
            ("Add Task", self.add_task),
            ("Edit Task", self.edit_task),
            ("Delete Task", self.delete_task)
        ]
        
        for text, command in buttons:
            ttk.Button(btn_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

        # Bind double-click event
        self.tree.bind('<Double-1>', lambda e: self.edit_task())

    def add_task(self):
        self.open_task_dialog()

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit")
            return
        self.open_task_dialog(self.tree.item(selected[0])['values'][0])

    def open_task_dialog(self, task_id=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task" if task_id else "Add Task")
        dialog.geometry("400x300")
        dialog.configure(bg=DARK_BG)

        # Get existing task data if editing
        task_data = ["", "Pending", "Medium", ""] 
        if task_id:
            self.cursor.execute("SELECT task, status, priority, due_date FROM tasks WHERE id=?", (task_id,))
            task_data = self.cursor.fetchone()

        # Create form fields
        fields = [
            ("Task:", ttk.Entry(dialog, width=40)),
            ("Status:", ttk.Combobox(dialog, values=["Pending", "In Progress", "Completed"])),
            ("Priority:", ttk.Combobox(dialog, values=["High", "Medium", "Low"])),
            ("Due Date (YYYY-MM-DD):", ttk.Entry(dialog))
        ]

        # Place fields and set values
        for i, ((label_text, field), value) in enumerate(zip(fields, task_data)):
            ttk.Label(dialog, text=label_text).pack(pady=5)
            field.pack(pady=5)
            field.insert(0, value)

        def save():
            values = [f.get() for _, f in fields]
            if not values[0]:
                messagebox.showwarning("Warning", "Task cannot be empty")
                return
                
            if task_id:
                self.cursor.execute("""
                    UPDATE tasks SET task=?, status=?, priority=?, due_date=? WHERE id=?
                """, (*values, task_id))
            else:
                self.cursor.execute("""
                    INSERT INTO tasks (task, status, priority, due_date) VALUES (?,?,?,?)
                """, values)
            
            self.conn.commit()
            self.load_tasks()
            dialog.destroy()

        ttk.Button(dialog, text="Save", command=save).pack(pady=20)

    def delete_task(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Please select a task to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            task_id = self.tree.item(self.tree.selection()[0])['values'][0]
            self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            self.conn.commit()
            self.load_tasks()

    def load_tasks(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
