import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import os
import tkinter.font as font
import datetime  # Import the datetime module

def save_to_csv():
    with open("daily_schedule.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Hours", "To-Do List", "Completed"])
        for i in range(12):
            hours = hour_entries[i].get()
            todos = todo_entries[i].get("1.0", tk.END)  # Get text from Text widget
            completed = completed_vars[i].get()  # Get the state of the checkbox
            writer.writerow([hours, todos, completed])

    messagebox.showinfo("Saved", "Your schedule was saved to daily_schedule.csv")

def load_from_csv():
    if os.path.exists("daily_schedule.csv"):
        try:
            with open("daily_schedule.csv", 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                for i, row in enumerate(reader):
                    if i < 12:
                        hours, todos, completed = row
                        hour_entries[i].insert(0, hours)
                        todo_entries[i].insert("1.0", todos)  # Insert text into Text widget
                        completed_vars[i].set(int(completed))  # Set the checkbox state

        except Exception as e:
            messagebox.showerror("Error", f"Could not load schedule: {e}")

root = tk.Tk()
root.title("To-Do List Table")

# Dark theme colors
bg_color = "#333333"
fg_color = "white"
entry_bg = "#444444"
entry_fg = "white"
button_bg = "#555555"
button_fg = "white"
checkbox_bg = bg_color  # Match checkbox background to the main background
checkbox_fg = fg_color

root.configure(bg=bg_color)

# Font configuration
font_name = "Helvetica"  # Modern-looking font
font_size = 12
default_font = font.Font(family=font_name, size=font_size)

# Style configuration for ttk widgets
style = ttk.Style()
style.theme_use('clam')  # Use a theme that supports background configuration

style.configure("TLabel", background=bg_color, foreground=fg_color, font=default_font)
style.configure("TButton", background=button_bg, foreground=button_fg, font=default_font)
style.configure("TEntry", fieldbackground=entry_bg, foreground=entry_fg, background=entry_bg, font=default_font)
style.configure("TCheckbutton", background=checkbox_bg, foreground=checkbox_fg, font=default_font, indicatoron=True, padding=20)


hour_entries = []
todo_entries = []
completed_vars = []  # Store the variables for the checkboxes
checkboxes = []

# Date and Time display
def update_datetime():
    now = datetime.datetime.now()
    date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    datetime_label.config(text=date_time_string)
    datetime_label.after(1000, update_datetime)  # Update every 1000 ms (1 second)

datetime_label = ttk.Label(root, text="", font=default_font)
datetime_label.grid(row=0, column=0, columnspan=3, pady=5)  # Span across all columns
update_datetime()  # Start updating the date and time



for i in range(12):
    hour_entry = ttk.Entry(root, width=15, font=default_font)
    hour_entry.configure(background=entry_bg, foreground=entry_fg)
    hour_entry.grid(row=i+2, column=0, padx=5, pady=2, sticky='ew')
    hour_entries.append(hour_entry)

    todo_entry = tk.Text(root, width=30, height=3, background=entry_bg, foreground=entry_fg, font=default_font)  # Use tk.Text for multiline
    todo_entry.grid(row=i+2, column=1, padx=5, pady=2, sticky='ew')
    todo_entries.append(todo_entry)

    completed_vars.append(tk.IntVar())  # Create a variable to store the checkbox state
    checkbox = ttk.Checkbutton(root, variable=completed_vars[i])
    checkbox.grid(row=i+2, column=2, padx=5, pady=2, sticky='ew')
    checkboxes.append(checkbox)

  

load_from_csv()

root.mainloop()
