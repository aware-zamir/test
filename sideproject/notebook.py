import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json

class NotebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Notebook")
        self.root.geometry("900x700")

        # Dark Mode Theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_style()

        self.current_file = None
        self.autosave_file = "notebook_autosave.json"

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        self.notebook.bind("<ButtonRelease-1>", self.edit_tab_name)

        # Add New Tab Button
        self.add_tab_button = ttk.Button(root, text="+", command=self.new_page)
        self.add_tab_button.pack(side="top", padx=10, pady=5)

        self.load_autosave()
        if self.notebook.index("end") == 0:
            self.new_page()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_style(self):
        bg_color = '#2e2e2e'
        fg_color = 'white'
        accent_color = '#555555'
        font = ('Segoe UI', 12)

        self.style.configure('TNotebook', background=bg_color, borderwidth=0)
        self.style.configure('TNotebook.Tab', background='#444444', foreground=fg_color, padding=[15, 7], font=font, borderwidth=0)
        self.style.map('TNotebook.Tab', background=[("selected", accent_color)], foreground=[("selected", fg_color)])

        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TButton', background='#444444', foreground=fg_color, borderwidth=0, padding=[10, 7], font=font)
        self.style.map('TButton', background=[("active", accent_color)])
        self.style.configure('TEntry', fieldbackground='#333333', foreground=fg_color, font=font, borderwidth=0)

        self.text_bg_color = '#333333'
        self.text_fg_color = fg_color
        self.text_font = ('Segoe UI', 13)

    def new_page(self, event=None):
        frame = ttk.Frame(self.notebook)
        text_widget = tk.Text(frame, wrap="word", undo=True, font=self.text_font, background=self.text_bg_color, foreground=self.text_fg_color, insertbackground=self.text_fg_color, relief='flat', bd=6, padx=10, pady=10)
        text_widget.pack(fill="both", expand=True)
        self.notebook.add(frame, text="New Tab")
        self.notebook.select(frame)

    def edit_tab_name(self, event=None):
        index = self.notebook.index("current")
        tab_text = self.notebook.tab(index, "text")

        popup = tk.Toplevel(self.root)
        popup.title("Rename Tab")
        popup.configure(bg='#2e2e2e')

        entry = ttk.Entry(popup)
        entry.insert(0, tab_text)
        entry.pack(padx=10, pady=10)

        def save_name():
            new_name = entry.get()
            if new_name:
                self.notebook.tab(index, text=new_name)
                popup.destroy()
            else:
                self.show_warning("Warning", "Tab name cannot be empty.")
        
        def delete_tab():
            if self.ask_yes_no("Confirm", "Are you sure you want to delete this tab?"):
                self.notebook.forget(index)
                popup.destroy()

        save_button = ttk.Button(popup, text="Save", command=save_name)
        save_button.pack(pady=5)
        
        delete_button = ttk.Button(popup, text="Delete", command=delete_tab)
        delete_button.pack(pady=5)

        popup.grab_set()
        popup.focus_set()
        popup.wait_window()

    def on_close(self):
        self.save_autosave()
        self.root.destroy()

    def save_autosave(self):
        data = []
        for i in range(self.notebook.index("end")):
            frame = self.notebook.winfo_children()[i]
            text_widget = frame.winfo_children()[0]
            content = text_widget.get("1.0", tk.END)
            tab_name = self.notebook.tab(i, "text")
            data.append({"tab_name": tab_name, "content": content})
        
        try:
            with open(self.autosave_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            self.show_error("Error", f"Could not save autosave data:\n{e}")

    def load_autosave(self):
        try:
            with open(self.autosave_file, "r") as f:
                data = json.load(f)
                for item in data:
                    frame = ttk.Frame(self.notebook)
                    text_widget = tk.Text(frame, wrap="word", undo=True, font=self.text_font, background=self.text_bg_color, foreground=self.text_fg_color, insertbackground=self.text_fg_color, relief='flat', bd=4)
                    text_widget.pack(fill="both", expand=True, padx=5, pady=5)
                    text_widget.insert("1.0", item["content"])
                    self.notebook.add(frame, text=item["tab_name"])
        except FileNotFoundError:
            pass
        except Exception as e:
            self.show_error("Error", f"Could not load autosave data:\n{e}")
            
    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        messagebox.showwarning(title, message)

    def ask_yes_no(self, title, message):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg='#2e2e2e')

        result = tk.BooleanVar()

        yes_button = ttk.Button(dialog, text="Yes", command=lambda: self.set_result(result, True, dialog))
        yes_button.pack(side=tk.LEFT, padx=5, pady=10)

        no_button = ttk.Button(dialog, text="No", command=lambda: self.set_result(result, False, dialog))
        no_button.pack(side=tk.RIGHT, padx=5, pady=10)

        message_label = tk.Label(dialog, text=message, bg='#2e2e2e', fg='white', font=('Arial', 12))
        message_label.pack(pady=10)

        dialog.grab_set()
        dialog.focus_set()
        dialog.wait_window()

        return result.get()

    def set_result(self, result_var, value, dialog):
        result_var.set(value)
        dialog.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#19191a')
    app = NotebookApp(root)
    root.mainloop()
