from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
from threading import Thread

# root window
root = tk.Tk()
root.geometry('600x600')
root.title('Progressbar Demo')

tk = tk.Button()

tk.grid(0, 0)


def update_progress_label():
    return f"Current Progress: {pb['value']}%"


def progress():
    if pb['value'] < 100:
        pb['value'] += 1
        value_label['text'] = update_progress_label()
    else:
        showinfo(message='The progress completed!')


def stop():
    pb.stop()
    value_label['text'] = update_progress_label()


# progressbar
pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=280
)
# place the progressbar
#pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

# label
value_label = ttk.Label(root, text=update_progress_label())
#value_label.grid(column=0, row=1, columnspan=2)


from time import sleep
def update_progress_bar():

    # You can write here your own logic how do you want to update your code.

    for i in range(100):
        progress()
        sleep(1)
    # -----------------------------------------------------------------------

t1 = Thread(target=update_progress_bar)
t1.start()


root.mainloop()