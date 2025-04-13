import tkinter as tk

window = tk.Tk()
window.title("My First GUI")
window.geometry("300x200")

label = tk.Label(window, text="Hello from Tkinter!")
label.pack()

window.mainloop()
