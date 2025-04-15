import tkinter as tk
from tkinter import ttk
import datetime

# Font scaling factor
FONT_SCALE = 1.1

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
    frame = ttk.Frame(parent, padding=10)
    
    # Datetime label at top
    datetime_label = ttk.Label(frame, font=scale_font(("Arial", 12)))
    datetime_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
    update_datetime(datetime_label)
    
    # Column Headers
    headers = ["Hour", "To-Do", "Completed", "Current Hour"]
    for col, text in enumerate(headers):
        ttk.Label(frame, text=text, font=scale_font(("Arial", 10, "bold"))).grid(
            row=1, column=col, padx=5, pady=5, sticky="w"
        )
    
    # Create 24 rows
    hour_entries = []
    todo_entries = []
    completed_vars = []
    clock_labels = []
    
    for i in range(24):
        # Hour input
        hour_entry = ttk.Entry(frame, width=15, font=scale_font(("Arial", 10)))
        hour_entry.insert(0, f"{str(i).zfill(2)}:00 - {str(i).zfill(2)}:59")  # Insert hour range
        hour_entry.grid(row=i+2, column=0, padx=5, pady=2, sticky="ew")
        hour_entries.append(hour_entry)
        
        # Todo entry
        todo_entry = tk.Text(frame, width=30, height=1, font=scale_font(("Arial", 10)), relief="solid", bd=1)
        todo_entry.grid(row=i+2, column=1, padx=5, pady=2, sticky="ew")
        todo_entries.append(todo_entry)
        
        # Checkbox for completed status
        var = tk.IntVar()
        checkbox = ttk.Checkbutton(frame, variable=var)
        checkbox.grid(row=i+2, column=2, padx=5, pady=2, sticky="ew")
        completed_vars.append(var)

        # Clock Label
        clock_label = ttk.Label(frame, font=scale_font(("Arial", 10)))
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
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Footer frame for buttons
        self.footer_frame = ttk.Frame(parent)
        self.footer_frame.pack(side="bottom", fill="x", padx=10, pady=5)
        
        # Create an "Add New Tab" button 
        self.add_tab_button = ttk.Button(self.footer_frame, text="+ Add Tab", command=self.new_page)
        self.add_tab_button.pack(side="left", padx=5, pady=2)
        
        # Add a "Remove Tab" button
        self.remove_tab_button = ttk.Button(self.footer_frame, text="- Remove Tab", command=self.remove_page)
        self.remove_tab_button.pack(side="left", padx=5, pady=2)
        
        self.new_page()
    
    def new_page(self, event=None):
        frame = ttk.Frame(self.notebook)
        text_widget = tk.Text(frame, wrap="word", undo=True,
                              font=scale_font(("Arial", 10)), relief="solid", bd=1, padx=5, pady=5)
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
    
    # Apply the general background color to the entire app
    
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
    main_notebook.add(notebook_frame, text="Notebook")
    notebook_app = NotebookTabApp(notebook_frame)
    
    root.protocol("WM_DELETE_WINDOW", lambda: on_app_close(root))
    root.mainloop()
