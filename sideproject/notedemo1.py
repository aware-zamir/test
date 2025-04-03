import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class NotebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Notebook")
        self.root.geometry("800x600")
        self.current_file = None

        # Dark Theme
        self.root.tk_setPalette(background="#2E2E2E", foreground="white", activeBackground="#5D6D7E", activeForeground="white")
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Menu Bar
        self.menu_bar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_page)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        root.config(menu=self.menu_bar)

        self.new_page()  # Start with one default page

    def new_page(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="New Page")
        text_widget = tk.Text(frame, wrap="word", undo=True, font=("Arial", 12, "bold"), background="#2E2E2E", foreground="white", insertbackground="white")
        text_widget.pack(fill="both", expand=True)
        self.notebook.select(frame)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                self.new_page()
                current_frame = self.notebook.nametowidget(self.notebook.select())
                text_widget = current_frame.winfo_children()[0]
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", content)
                self.current_file = file_path
                self.notebook.tab(self.notebook.select(), text=os.path.basename(file_path))
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{e}")

    def save_file(self):
        if self.current_file:
            try:
                current_frame = self.notebook.nametowidget(self.notebook.select())
                text_widget = current_frame.winfo_children()[0]
                content = text_widget.get("1.0", tk.END)
                with open(self.current_file, "w") as file:
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                current_frame = self.notebook.nametowidget(self.notebook.select())
                text_widget = current_frame.winfo_children()[0]
                content = text_widget.get("1.0", tk.END)
                with open(file_path, "w") as file:
                    file.write(content)
                self.current_file = file_path
                self.notebook.tab(self.notebook.select(), text=os.path.basename(file_path))
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotebookApp(root)
    root.mainloop()