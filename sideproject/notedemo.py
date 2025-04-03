import tkinter as tk
from tkinter import simpledialog

class DarkModeNotebook:
    def __init__(self, root):
        self.root = root
        self.root.title("Dark Mode Notebook")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#121212")

        # Sidebar for notes
        self.sidebar = tk.Frame(self.root, bg="#1E1E1E", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.notes_list = tk.Listbox(self.sidebar, bg="#1E1E1E", fg="white", font=("Arial", 12), selectbackground="#333333")
        self.notes_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.notes_list.bind("<<ListboxSelect>>", self.open_note)

        self.add_note_button = tk.Button(self.sidebar, text="Add Note", bg="#333333", fg="white", font=("Arial", 12, "bold"), command=self.add_note)
        self.add_note_button.pack(fill=tk.X, padx=10, pady=5)

        # Main page for note content
        self.main_page = tk.Text(self.root, bg="#121212", fg="white", font=("Arial", 14), insertbackground="white", wrap=tk.WORD)
        self.main_page.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.notes = {}

    def add_note(self):
        note_title = simpledialog.askstring("New Note", "Enter note title:", parent=self.root)
        if note_title:
            self.notes[note_title] = ""
            self.notes_list.insert(tk.END, note_title)

    def open_note(self, event):
        selected = self.notes_list.curselection()
        if selected:
            note_title = self.notes_list.get(selected)
            self.main_page.delete(1.0, tk.END)
            self.main_page.insert(tk.END, self.notes[note_title])

            # Save changes to the note when switching
            def save_note_content(event):
                self.notes[note_title] = self.main_page.get(1.0, tk.END).strip()

            self.main_page.bind("<FocusOut>", save_note_content)

if __name__ == "__main__":
    root = tk.Tk()
    app = DarkModeNotebook(root)
    root.mainloop()