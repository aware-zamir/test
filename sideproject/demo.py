import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as font
import datetime
import os
import pickle

# Modern Dark Theme Colors - Increased Contrast
BG_COLOR = "#1E1E1E"  # Deeper dark background
FG_COLOR = "#FFFFFF"  # Brighter white text
ENTRY_BG = "#333333"  # Slightly lighter than BG
ENTRY_FG = "#FFFFFF"  # Brighter white text
BUTTON_BG = "#282828"  # Darker button background
BUTTON_FG = "#FFFFFF"  # Brighter white text
ACCENT_COLOR = "#777777"  # Dark gray accent color for focus/active states

# Utility: update a label with current date/time every second
def update_datetime(label):
    now = datetime.datetime.now()
    label.config(text=now.strftime("%Y-%m-%d %H:%M:%S"))
    label.after(1000, update_datetime, label)

# Create the To-Do List Table as a frame to add into a Notebook tab
def create_todo_tab(parent):
    frame = ttk.Frame(parent)
    frame.configure(style='Custom.TFrame')
    
    # Datetime label at top
    datetime_label = ttk.Label(frame, font=("Helvetica", 18), background=BG_COLOR, foreground=FG_COLOR)
    datetime_label.grid(row=0, column=0, columnspan=3, pady=5)
    update_datetime(datetime_label)
    
    # Create 12 rows
    hour_entries = []
    todo_entries = []
    completed_vars = []
    
    for i in range(12):
        # Hour input using ttk.Entry
        hour_entry = ttk.Entry(frame, width=15, style='Dark.TEntry')
        hour_entry.grid(row=i+1, column=0, padx=5, pady=2, sticky="ew")
        hour_entries.append(hour_entry)
        
        # Todo entry using tk.Text for multiline support. Use provided dark colors.
        todo_entry = tk.Text(frame, width=30, height=3, background=ENTRY_BG, 
                             foreground=ENTRY_FG, font=("Helvetica", 12), insertbackground=FG_COLOR)
        todo_entry.grid(row=i+1, column=1, padx=5, pady=2, sticky="ew")
        todo_entries.append(todo_entry)
        
        # Checkbox for completed status
        var = tk.IntVar()
        checkbox = ttk.Checkbutton(frame, variable=var, style='Dark.TCheckbutton')
        checkbox.grid(row=i+1, column=2, padx=5, pady=2, sticky="ew")
        completed_vars.append(var)
    
    frame.columnconfigure(1, weight=1)
    return frame, hour_entries, todo_entries, completed_vars

# NotebookTabApp: a container inside the second tab that implements a multipage notebook with autosave.
class NotebookTabApp:
    def __init__(self, parent):
        self.parent = parent
        self.autosave_file = "notebook_autosave.pkl"
        self.current_file = None
        self.tab_count = 1  # Initialize tab counter
        
        # Create an internal Notebook widget
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.configure_style()
        
        # Create an "Add New Tab" button above the internal notebook
        self.add_tab_button = ttk.Button(parent, text="+", command=self.new_page, style="Accent.TButton")
        self.add_tab_button.pack(padx=10, pady=5, anchor="ne")
        
        # Add a "Remove Tab" button
        self.remove_tab_button = ttk.Button(parent, text="-", command=self.remove_page, style="Accent.TButton")
        self.remove_tab_button.pack(padx=10, pady=5, anchor="ne")
        
        self.load_autosave()
        #if self.notebook.index("end") == 0:
        #    self.new_page()
    
    def configure_style(self):
        style = ttk.Style()
        bg_color = BG_COLOR
        fg_color = FG_COLOR
        accent_color = ACCENT_COLOR
        myfont = ("Segoe UI", 12)
        
        # Notebook styling
        style.configure("TNotebook", background=bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=ENTRY_BG, foreground=fg_color,
                        padding=[15, 7], font=myfont, borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", accent_color)], 
                  foreground=[("selected", fg_color)],
                  expand=[("selected", [1, 1, 1, 0])])  # Expand the selected tab
        
        # Frame styling
        style.configure("TFrame", background=bg_color)
        
        # Button styling
        style.configure("TButton", background=BUTTON_BG, foreground=fg_color,
                        borderwidth=0, padding=[10, 7], font=myfont)
        style.map("TButton", background=[("active", ACCENT_COLOR)])
        
        # Accent Button styling
        style.configure("Accent.TButton", background=accent_color, foreground=fg_color,
                        borderwidth=0, padding=[10, 7], font=myfont)
        style.map("Accent.TButton", background=[("active", "#666666")])
        
        # Entry styling
        style.configure("Dark.TEntry", fieldbackground=ENTRY_BG, foreground=ENTRY_FG,
                        borderwidth=0, padding=[5])
        
        # Checkbutton styling
        style.configure("Dark.TCheckbutton", background=bg_color, foreground=fg_color)
        
        self.text_bg_color = ENTRY_BG
        self.text_fg_color = fg_color
        self.text_font = ("Segoe UI", 13)
    
    def new_page(self, event=None):
        frame = ttk.Frame(self.notebook)
        frame.configure(style="TFrame")
        text_widget = tk.Text(frame, wrap="word", undo=True,
                              font=self.text_font, background=self.text_bg_color,
                              foreground=self.text_fg_color, insertbackground=self.text_fg_color,
                              relief="flat", bd=6, padx=10, pady=10)
        text_widget.pack(fill="both", expand=True)
        self.notebook.add(frame, text=str(self.tab_count))  # Use tab counter as tab name
        self.notebook.select(frame)
        self.tab_count += 1  # Increment tab counter
    
    def remove_page(self):
        selected_tab = self.notebook.select()
        if selected_tab:
            self.notebook.forget(selected_tab)
            if self.notebook.index("end") == 0:
                self.tab_count = 1
    
    def load_autosave(self):
        try:
            with open(self.autosave_file, "rb") as f:
                data = pickle.load(f)
                for item in data:
                    frame = ttk.Frame(self.notebook)
                    text_widget = tk.Text(frame, wrap="word", undo=True,
                                          font=self.text_font, background=self.text_bg_color,
                                          foreground=self.text_fg_color, insertbackground=self.text_fg_color,
                                          relief="flat", bd=4)
                    text_widget.pack(fill="both", expand=True, padx=5, pady=5)
                    text_widget.insert("1.0", item["content"])
                    self.notebook.add(frame, text=item["tab_name"])
                    
                    # Update tab_count to the highest loaded tab number + 1
                    try:
                        tab_number = int(item["tab_name"])
                        self.tab_count = max(self.tab_count, tab_number + 1)
                    except ValueError:
                        # Handle the case where the tab name is not an integer
                        pass
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Could not load autosave data:\n{e}")
    
    def save_autosave(self):
        data = []
        for i in range(self.notebook.index("end")):
            frame = self.notebook.winfo_children()[i]
            text_widget = frame.winfo_children()[0]
            content = text_widget.get("1.0", tk.END)
            tab_name = self.notebook.tab(i, "text")
            data.append({"tab_name": tab_name, "content": content})
        try:
            with open(self.autosave_file, "wb") as f:
                pickle.dump(data, f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save autosave data:\n{e}")

    # This method can be extended to integrate Save/Open menu commands if needed.
    
TODO_AUTOSAVE_FILE = "todo_autosave.pkl"

def on_app_close(root, notebook_app, hour_entries, todo_entries, completed_vars):
    # Save Notebook tab data
    notebook_app.save_autosave()
    
    # Save To-Do List tab data
    todo_data = []
    for i in range(12):
        todo_data.append({
            "hour": hour_entries[i].get(),
            "todo": todo_entries[i].get("1.0", tk.END),
            "completed": completed_vars[i].get()
        })
    try:
        with open(TODO_AUTOSAVE_FILE, "wb") as f:
            pickle.dump(todo_data, f)
    except Exception as e:
        messagebox.showerror("Error", f"Could not save To-Do List data:\n{e}")
    
    root.destroy()

def load_todo_data(hour_entries, todo_entries, completed_vars):
    try:
        with open(TODO_AUTOSAVE_FILE, "rb") as f:
            todo_data = pickle.load(f)
            for i in range(12):
                hour_entries[i].insert(0, todo_data[i]["hour"])
                todo_entries[i].insert("1.0", todo_data[i]["todo"])
                completed_vars[i].set(todo_data[i]["completed"])
    except FileNotFoundError:
        pass
    except Exception as e:
        messagebox.showerror("Error", f"Could not load To-Do List data:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Integrated App")
    root.configure(bg=BG_COLOR)
    style = ttk.Style(root)
    style.theme_use("clam")
    
    # Apply the general background color to the entire app
    root.configure(bg=BG_COLOR)
    style.configure("TNotebook", background=BG_COLOR)
    style.configure("TFrame", background=BG_COLOR)
    
    # Create the main notebook with two tabs
    main_notebook = ttk.Notebook(root)
    main_notebook.pack(fill="both", expand=True)
    
    # Tab 1: To-Do List Table (Hour List)
    todo_frame, hour_entries, todo_entries, completed_vars = create_todo_tab(main_notebook)
    main_notebook.add(todo_frame, text="To-Do List")
    
    # Tab 2: Modern Notebook
    notebook_frame = ttk.Frame(main_notebook)
    notebook_frame.configure(style="TFrame")
    main_notebook.add(notebook_frame, text="Notebook")
    notebook_app = NotebookTabApp(notebook_frame)
    
    # Load To-Do List data
    load_todo_data(hour_entries, todo_entries, completed_vars)
    
    root.protocol("WM_DELETE_WINDOW", lambda: on_app_close(root, notebook_app, hour_entries, todo_entries, completed_vars))
    root.mainloop()