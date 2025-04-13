import tkinter as tk
from tkinter import ttk
import datetime

# Modern Dark Theme Colors - Shades of Gray
BG_COLOR = "#333333"  # Darker background
FG_COLOR = "#D4D4D4"  # Lighter foreground for better contrast
ENTRY_BG = "#4A4A4A"  # Slightly lighter than BG_COLOR
ENTRY_FG = "#E0E0E0"  # Even lighter text for entries
BUTTON_BG = "#666666"  # Medium gray for buttons
BUTTON_FG = "#FAFAFA"  # Very light foreground for buttons
ACCENT_COLOR = "#808080"  # A neutral gray for accent

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
    datetime_label.grid(row=0, column=0, columnspan=3, pady=10)  # Increased padding
    update_datetime(datetime_label)
    
    # Column Headers
    ttk.Label(frame, text="Hour", background=BG_COLOR, foreground=FG_COLOR, font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)
    ttk.Label(frame, text="To-Do", background=BG_COLOR, foreground=FG_COLOR, font=("Helvetica", 12)).grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(frame, text="Completed", background=BG_COLOR, foreground=FG_COLOR, font=("Helvetica", 12)).grid(row=1, column=2, padx=5, pady=5)
    
    # Create 12 rows
    hour_entries = []
    todo_entries = []
    completed_vars = []
    
    for i in range(12):
        # Hour input using ttk.Entry
        hour_entry = ttk.Entry(frame, width=10, style='Dark.TEntry')  # Increased width
        hour_entry.grid(row=i+2, column=0, padx=5, pady=5, sticky="ew")  # Adjusted row and padding
        hour_entries.append(hour_entry)
        
        # Todo entry using tk.Text for multiline support. Use provided dark colors.
        todo_entry = tk.Text(frame, width=40, height=2, background=ENTRY_BG, 
                             foreground=ENTRY_FG, font=("Helvetica", 12), insertbackground=FG_COLOR,
                             relief="flat", bd=4)  # Added relief and border
        todo_entry.grid(row=i+2, column=1, padx=5, pady=5, sticky="ew")  # Adjusted row and padding
        todo_entries.append(todo_entry)
        
        # Checkbox for completed status
        var = tk.IntVar()
        checkbox = ttk.Checkbutton(frame, variable=var, style='Dark.TCheckbutton')
        checkbox.grid(row=i+2, column=2, padx=5, pady=5, sticky="ew")  # Adjusted row and padding
        completed_vars.append(var)
    
    frame.columnconfigure(1, weight=1)
    return frame, hour_entries, todo_entries, completed_vars

# NotebookTabApp: a container inside the second tab that implements a multipage notebook.
class NotebookTabApp:
    def __init__(self, parent):
        self.parent = parent
        self.tab_count = 1  # Initialize tab counter
        
        # Create an internal Notebook widget
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.configure_style()
        
        # Create an "Add New Tab" button above the internal notebook
        self.add_tab_button = ttk.Button(parent, text="+ Add Tab", command=self.new_page, style="Accent.TButton")
        self.add_tab_button.pack(padx=10, pady=5, anchor="nw")  # Moved anchor
        
        # Add a "Remove Tab" button
        self.remove_tab_button = ttk.Button(parent, text="- Remove Tab", command=self.remove_page, style="Accent.TButton")
        self.remove_tab_button.pack(padx=10, pady=5, anchor="nw")  # Moved anchor
        
        self.new_page()
    
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
        self.notebook.add(frame, text=f"Tab {self.tab_count}")  # Use tab counter as tab name
        self.notebook.select(frame)
        self.tab_count += 1  # Increment tab counter
    
    def remove_page(self):
        selected_tab = self.notebook.select()
        if selected_tab:
            self.notebook.forget(selected_tab)
            if self.notebook.index("end") == 0:
                self.tab_count = 1

def on_app_close(root):
    root.destroy()

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
    
    # Make the window full screen
    root.state('zoomed')  # For Windows
    # root.attributes('-fullscreen', True) # For Linux and macOS
    
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
    
    root.protocol("WM_DELETE_WINDOW", lambda: on_app_close(root))
    root.mainloop()
