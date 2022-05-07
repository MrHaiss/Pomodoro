import math
import tkinter as tk
import time

# Globals
PINK = "#e2979c"
RED = "#e7305b"
DARK_GREEN = "#013220"
GREEN = "#4d8c57"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
LOOPS = 0
TIMER_RUNNING = False
ACTIVE_TIMER = None


# Button on clicks
def start_button_click():
    global LOOPS
    global TIMER_RUNNING
    LOOPS += 1

    # If odd, then work
    if LOOPS % 2 != 0 and not TIMER_RUNNING:
        countdown(WORK_MIN * 60)
        header.config(text="Work", fg=GREEN)
    # If even but not the 8th cycle, take a short break
    elif LOOPS % 2 == 0 and LOOPS % 8 != 0 and not TIMER_RUNNING:
        countdown(SHORT_BREAK_MIN * 60)
        header.config(text="Short Break", fg=PINK)
    # If even and the 8th cycle, take a long break
    elif LOOPS % 2 == 0 and LOOPS % 8 == 0 and not TIMER_RUNNING:
        countdown(LONG_BREAK_MIN * 60)
        header.config(text="Long Break", fg=RED)

    TIMER_RUNNING = True


def reset_button_click():
    global LOOPS
    global TIMER_RUNNING
    global ACTIVE_TIMER

    tick.config(text="")
    header.config(text="Timer")
    canvas.itemconfig(timer_text,text="00:00")
    LOOPS = 0
    TIMER_RUNNING = False

    window.after_cancel(ACTIVE_TIMER)


# UI setup
window = tk.Tk()
window.title("Pomodoro App")
window.config(padx=80, pady=35, bg=YELLOW)
window.resizable(False, False)

header = tk.Label(text="Timer", bg=YELLOW, fg=DARK_GREEN, font=(FONT_NAME, 30, "bold"))
header.grid(row=1, column=2)

canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
src_tomato = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=src_tomato)
timer_text = canvas.create_text(108, 125, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))
canvas.grid(row=2, column=2)

start_button = tk.Button(text="Start", command=start_button_click)
start_button.grid(row=3, column=1)

reset_button = tk.Button(text="Reset", command=reset_button_click)
reset_button.grid(row=3, column=4)

tick = tk.Label(text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
tick.grid(row=4, column=2)


# Timer management
def countdown(count):
    global LOOPS
    global TIMER_RUNNING
    global ACTIVE_TIMER

    count_formatted = time.strftime("%M:%S", time.gmtime(count))
    canvas.itemconfig(timer_text, text=count_formatted)
    if count > 0:
        ACTIVE_TIMER = window.after(1000, countdown, count - 1)
    else:
        TIMER_RUNNING = False
        work_cycles = math.floor(LOOPS / 2)
        ticks = ""
        for c in range(work_cycles):
            ticks += "✔"

        tick.config(text=ticks)
        start_button_click()


# Runtime
window.mainloop()
