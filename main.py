import tkinter
import random
from pathlib import Path
import pandas as pd
import time

# -----
# Configs
# -----
BACKGROUND_COLOR = "#B1DDC6"
CARD_FRONT = Path().cwd() / "images" / "card_front.png"
CARD_BACK = Path().cwd() / "images" / "card_back.png"
CORRECT_IMAGE = Path().cwd() / "images" / "right.png"
BAD_IMAGE = Path().cwd() / "images" / "wrong.png"
WORDS_PATH = Path().cwd() / "data" / "french_words.csv"
WORDS_TO_LEARN = Path().cwd() / "data" / "words_to_learn.csv"
current_card = {}

# -----
# Read words/translations
# -----
try:
    df = pd.read_csv(WORDS_TO_LEARN)
except FileNotFoundError:
    df = pd.read_csv(WORDS_PATH)
    to_learn = df.to_dict(orient="records")
else:
    to_learn = df.to_dict(orient="records")


# -----
# generate random word
# -----
def next_card():
    global current_card
    global flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    # print(new_word)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def next_card_ok():
    global current_card
    to_learn.remove(current_card)
    # write the file
    with open(WORDS_TO_LEARN, mode="w") as f:
        f.write("French,English\n")
        for item in to_learn:
            f.write(f"{item['French']},{item['English']}\n")

    next_card()


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=card_back_image)


# -----
# UI
# -----

window = tkinter.Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")

flip_timer = window.after(3000, func=flip_card)

# Card
canvas = tkinter.Canvas(width=800, height=526)
card_front_image = tkinter.PhotoImage(file=CARD_FRONT)
card_back_image = tkinter.PhotoImage(file=CARD_BACK)
canvas_image = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"), fill="black")

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
right_image = tkinter.PhotoImage(file=CORRECT_IMAGE)
right_button = tkinter.Button(image=right_image, highlightthickness=0, command=next_card_ok)
right_button.grid(row=1, column=1)

wrong_image = tkinter.PhotoImage(file=BAD_IMAGE)
wrong_button = tkinter.Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
