#main.py

from tkinter import *
import json
from tkinter import messagebox
from pyswip import Prolog

# Load story from JSON
with open("story.json") as f:
    story = json.load(f)

# Load Prolog logic
prolog = Prolog()
prolog.consult("logic.pl")

# Query Prolog for valid transitions
def get_next(current, choice):
    query = f"path('{current}', '{choice}', Next)."
    result = list(prolog.query(query))
    return result[0]["Next"] if result else None

# GUI setup
root = Tk()
root.title("AI Dungeon Builder")
root.geometry("500x300")

prompt = StringVar()
prompt.set("")

prompt_label = Label(root, textvariable=prompt, wraplength=450, justify=LEFT, font=("Arial", 12))
prompt_label.pack(pady=20)

options_frame = Frame(root)
options_frame.pack()

current_state = "start"

def load_state(state):
    global current_state
    current_state = state
    scene = story[state]
    prompt.set(scene["prompt"])
    for widget in options_frame.winfo_children():
        widget.destroy()
    for opt in scene["options"]:
        Button(options_frame, text=opt, width=20,
               command=lambda o=opt: on_choice(o)).pack(pady=2)

def on_choice(choice):
    global current_state
    next_state = get_next(current_state, choice)
    if next_state:
        load_state(next_state)
    else:
        messagebox.showinfo("End", "The story ends here.")

# Start game
load_state("start")
root.mainloop()