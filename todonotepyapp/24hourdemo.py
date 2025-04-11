import tkinter as tk
from tkinter import ttk
import datetime

# Modern Dark Theme Colors
BG_COLOR = "#1E1E1E"
FG_COLOR = "#FFFFFF"
ENTRY_BG = "#2D2D2D"
ENTRY_FG = "#E0E0E0"
BUTTON_BG = "#3A3A3A"
BUTTON_FG = "#FFFFFF"
ACCENT_COLOR = "#444444"  # Changed to dark gray

# Font scaling factor
FONT_SCALE = 1.2  # Increase font size by 20%

def scale_font(font_tuple):
    """Scales a font size by the FONT_SCALE factor."""
    name, size, *options = font_tuple
    scaled_size = int(size * FONT_SCALE)
    return (name, scaled_size, *options)

# Utility: update a label with current date/time every second
def update_datetime(label):
    now = datetime.datetime.now()
    label.config(text=now.strftime("%Y-%m-%d %H:%M:%S"))
    label.after(1000, update_datetime, label)

# Create the To-Do List Table
def create_todo_tab(parent):
    frame = ttk.Frame(parent)
    frame.configure(style='Custom.TFrame')
    
    # Datetime label at top
    datetime_label = ttk.Label(frame, font=scale_font(("Roboto", 12)), background=BG_COLOR, foreground=FG_COLOR)
    datetime_label.grid(row=0, column=0, columnspan=3, pady=5)
    update_datetime(datetime_label)
    
    # Column Headers
    headers = ["Hour", "To-Do", "Completed", "Current Hour"]
    for col, text in enumerate(headers):
        ttk.Label(frame, text=text, background=BG_COLOR, foreground=FG_COLOR, font=scale_font(("Roboto", 9, "bold"))).grid(
            row=1, column=col, padx=5, pady=2, sticky="w"
        )
    
    # Create 24 rows
    hour_entries = []
    todo_entries = []
    completed_vars = []
    clock_labels = []
    
    for i in range(24):
        # Hour input
        hour_entry = ttk.Entry(frame, width=15, style='Dark.TEntry', font=scale_font(("Roboto", 9)))
        hour_entry.insert(0, f"{str(i).zfill(2)}:00 {str(i).zfill(2)}:59")  # Insert hour range
        hour_entry.grid(row=i+2, column=0, padx=5, pady=2, sticky="ew")
        hour_entries.append(hour_entry)
        
        # Todo entry
        todo_entry = tk.Text(frame, width=30, height=1, background=ENTRY_BG, 
                             foreground=ENTRY_FG, font=scale_font(("Roboto", 9)), insertbackground=FG_COLOR,
                             relief="flat", bd=2)
        todo_entry.grid(row=i+2, column=1, padx=5, pady=2, sticky="ew")
        todo_entries.append(todo_entry)
        
        # Checkbox for completed status
        var = tk.IntVar()
        checkbox = ttk.Checkbutton(frame, variable=var, style='Dark.TCheckbutton')
        checkbox.grid(row=i+2, column=2, padx=5, pady=2, sticky="ew")
        completed_vars.append(var)

        # Clock Label
        clock_label = ttk.Label(frame, background=BG_COLOR, foreground=FG_COLOR, font=scale_font(("Roboto", 9)))
        clock_label.grid(row=i+2, column=3, padx=5, pady=2, sticky="ew")
        clock_labels.append(clock_label)
    
    def update_clocks():
        now = datetime.datetime.now()
        current_hour = now.hour
        for i, clock_label in enumerate(clock_labels):
            if i == current_hour:
                clock_label.config(text=now.strftime("%H:%M:%S"))  # Show current time
            else:
                clock_label.config(text="")  # Clear other labels
        frame.after(1000, update_clocks)  # Update every 1000 ms (1 second)

    update_clocks()  # Start the clock update loop
    
    frame.columnconfigure(1, weight=1)
    return frame, hour_entries, todo_entries, completed_vars

# NotebookTabApp: a container inside the second tab that implements a multipage notebook.
class NotebookTabApp:
    def __init__(self, parent):
        self.parent = parent
        self.tab_count = 1
        
        # Create an internal Notebook widget
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.configure_style()
        
        # Footer frame for buttons
        self.footer_frame = ttk.Frame(parent)
        self.footer_frame.pack(side="bottom", fill="x", padx=5, pady=2)
        
        # Create an "Add New Tab" button 
        self.add_tab_button = ttk.Button(self.footer_frame, text="+ Add Tab", command=self.new_page, style="Accent.TButton")
        self.add_tab_button.pack(side="left", padx=5, pady=2)
        
        # Add a "Remove Tab" button
        self.remove_tab_button = ttk.Button(self.footer_frame, text="- Remove Tab", command=self.remove_page, style="Accent.TButton")
        self.remove_tab_button.pack(side="left", padx=5, pady=2)
        
        self.new_page()
    
    def configure_style(self):
        style = ttk.Style()
        
        # Notebook styling
        style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", background=ENTRY_BG, foreground=FG_COLOR,
                        padding=[8, 4], font=scale_font(("Roboto", 9)), borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", ACCENT_COLOR)], 
                  foreground=[("selected", FG_COLOR)])
        
        # Frame styling
        style.configure("TFrame", background=BG_COLOR)
        
        # Button styling
        style.configure("TButton", background=BUTTON_BG, foreground=FG_COLOR,
                        borderwidth=0, padding=[5, 4], font=scale_font(("Roboto", 9)))
        style.map("TButton", background=[("active", ACCENT_COLOR)])
        
        # Accent Button styling
        style.configure("Accent.TButton", background=ACCENT_COLOR, foreground=FG_COLOR,
                        borderwidth=0, padding=[5, 4], font=scale_font(("Roboto", 9)))
        style.map("Accent.TButton", background=[("active", "#005A9E")])
        
        # Entry styling
        style.configure("Dark.TEntry", fieldbackground=ENTRY_BG, foreground=ENTRY_FG,
                        borderwidth=0, padding=[3], font=scale_font(("Roboto", 9)))
        
        # Checkbutton styling
        style.configure("Dark.TCheckbutton", background=BG_COLOR, foreground=FG_COLOR, font=scale_font(("Roboto", 9)))
        
        self.text_bg_color = ENTRY_BG
        self.text_fg_color = FG_COLOR
        self.text_font = scale_font(("Roboto", 10))
    
    def new_page(self, event=None):
        frame = ttk.Frame(self.notebook)
        frame.configure(style="TFrame")
        text_widget = tk.Text(frame, wrap="word", undo=True,
                              font=self.text_font, background=self.text_bg_color,
                              foreground=self.text_fg_color, insertbackground=self.text_fg_color,
                              relief="flat", bd=3, padx=5, pady=5)
        text_widget.pack(fill="both", expand=True)
        self.notebook.add(frame, text=f"Tab {self.tab_count}")
        self.notebook.select(frame)
        self.tab_count += 1
    
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
    
    # Make the window full screen
    root.state('zoomed')
    
    # Create the main notebook with two tabs
    main_notebook = ttk.Notebook(root)
    main_notebook.pack(fill="both", expand=True)
    
    # Tab 1: To-Do List Table
    todo_frame, hour_entries, todo_entries, completed_vars = create_todo_tab(main_notebook)
    main_notebook.add(todo_frame, text="To-Do List")
    
    # Tab 2: Modern Notebook
    notebook_frame = ttk.Frame(main_notebook)
    notebook_frame.configure(style="TFrame")
    main_notebook.add(notebook_frame, text="Notebook")
    notebook_app = NotebookTabApp(notebook_frame)
    
    root.protocol("WM_DELETE_WINDOW", lambda: on_app_close(root))
    root.mainloop()
