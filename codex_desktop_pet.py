"""A tiny, local-only desktop companion for Windows.

Run with:  py codex_desktop_pet.py
Click the pet to chat.  Drag it by its body.  Right-click it for controls.
"""

from __future__ import annotations

import random
import tkinter as tk
from datetime import datetime

sd
BG = "#f5f0ff"          # A single colour made transparent by Windows Tk.
INK = "#27213a"
PURPLE = "#7655d6"
LILAC = "#d9cdff"
PEACH = "#ffd9c9"


class CodexPet:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Codex Buddy")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=BG)
        # Supported by standard Tk builds on Windows. It makes the window look
        # like a true desktop pet rather than a rectangular mini-window.
        self.root.wm_attributes("-transparentcolor", BG)
        self.root.geometry("250x285+1080+620")

        self.canvas = tk.Canvas(self.root, width=250, height=285, bg=BG,
                                highlightthickness=0)
        self.canvas.pack()
        self.mood = "ready"
        self.eye_open = True
        self.bob = 0
        self.drag_x = 0
        self.drag_y = 0
        self.message_id: int | None = None

        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.canvas.bind("<Button-3>", self.show_menu)
        self.menu = tk.Menu(self.root, tearoff=False, font=("Segoe UI", 10))
        self.menu.add_command(label="Chat with Codex Buddy", command=self.chat)
        self.menu.add_command(label="What can you do?", command=self.introduce)
        self.menu.add_separator()
        self.menu.add_command(label="Quit", command=self.root.destroy)

        self.draw()
        self.animate()

    def draw(self) -> None:
        self.canvas.delete("all")
        y = self.bob
        # Shadow and round hoodie/robot body.
        self.canvas.create_oval(55, 236 + y, 195, 258 + y, fill="#d1c7e6", outline="")
        self.canvas.create_oval(58, 88 + y, 192, 225 + y, fill=PURPLE, outline=INK, width=3)
        self.canvas.create_oval(72, 61 + y, 178, 170 + y, fill=LILAC, outline=INK, width=3)
        self.canvas.create_oval(84, 74 + y, 166, 151 + y, fill="#fffaff", outline="")
        # Ears.
        self.canvas.create_oval(57, 101 + y, 88, 137 + y, fill=PEACH, outline=INK, width=3)
        self.canvas.create_oval(162, 101 + y, 193, 137 + y, fill=PEACH, outline=INK, width=3)
        # Eyes and expression.
        if self.eye_open:
            self.canvas.create_oval(100, 104 + y, 111, 120 + y, fill=INK, outline="")
            self.canvas.create_oval(139, 104 + y, 150, 120 + y, fill=INK, outline="")
        else:
            self.canvas.create_line(99, 113 + y, 112, 113 + y, fill=INK, width=3)
            self.canvas.create_line(138, 113 + y, 151, 113 + y, fill=INK, width=3)
        self.canvas.create_arc(113, 117 + y, 137, 137 + y, start=200, extent=140,
                               style="arc", outline=INK, width=3)
        self.canvas.create_text(125, 188 + y, text="CODEX", fill="white",
                                font=("Segoe UI", 12, "bold"))
        self.canvas.create_text(125, 212 + y, text="your tiny coding buddy",
                                fill="#eee9ff", font=("Segoe UI", 8))
        if self.message_id is None:
            self.canvas.create_text(125, 34, text="Click me to chat", fill=INK,
                                    font=("Segoe UI", 10, "bold"))

    def animate(self) -> None:
        self.bob = 2 if self.bob == 0 else 0
        self.draw()
        self.root.after(700, self.animate)
        if random.randint(1, 14) == 1:
            self.blink()

    def blink(self) -> None:
        self.eye_open = False
        self.draw()
        self.root.after(160, self.open_eyes)

    def open_eyes(self) -> None:
        self.eye_open = True
        self.draw()

    def start_drag(self, event: tk.Event) -> None:
        self.drag_x, self.drag_y = event.x, event.y

    def drag(self, event: tk.Event) -> None:
        x = self.root.winfo_x() + event.x - self.drag_x
        y = self.root.winfo_y() + event.y - self.drag_y
        self.root.geometry(f"+{x}+{y}")

    def end_drag(self, event: tk.Event) -> None:
        # A click has very little pointer movement; open the chat in that case.
        if abs(event.x - self.drag_x) < 5 and abs(event.y - self.drag_y) < 5:
            self.chat()

    def show_menu(self, event: tk.Event) -> None:
        self.menu.tk_popup(event.x_root, event.y_root)

    def say(self, message: str) -> None:
        if self.message_id is not None:
            self.canvas.delete("speech")
        self.canvas.create_rectangle(10, 5, 240, 57, fill="white", outline=PURPLE,
                                     width=2, tags="speech")
        self.canvas.create_polygon(116, 57, 134, 57, 125, 68, fill="white",
                                   outline=PURPLE, tags="speech")
        self.canvas.create_text(125, 30, text=message, width=208, fill=INK,
                                font=("Segoe UI", 9), tags="speech")
        self.message_id = 1
        self.root.after(6000, self.clear_speech)

    def clear_speech(self) -> None:
        self.canvas.delete("speech")
        self.message_id = None
        self.draw()

    def introduce(self) -> None:
        self.say("I am your local Codex Buddy. Click me whenever you need a nudge!")

    def chat(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Chat with Codex Buddy")
        dialog.attributes("-topmost", True)
        dialog.resizable(False, False)
        dialog.configure(bg="#fbfaff", padx=14, pady=14)
        tk.Label(dialog, text="What are you working on?", bg="#fbfaff", fg=INK,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        entry = tk.Entry(dialog, width=42, font=("Segoe UI", 10))
        entry.pack(pady=(8, 10))
        entry.focus_set()

        def send(_: object = None) -> None:
            prompt = entry.get().strip()
            if not prompt:
                return
            dialog.destroy()
            self.reply(prompt)

        tk.Button(dialog, text="Send", command=send, bg=PURPLE, fg="white",
                  relief="flat", padx=16, pady=5).pack(anchor="e")
        dialog.bind("<Return>", send)

    def reply(self, prompt: str) -> None:
        lower = prompt.lower()
        if "time" in lower:
            message = f"It is {datetime.now().strftime('%I:%M %p')}. Keep going!"
        elif any(word in lower for word in ("bug", "error", "fix")):
            message = "Try: reproduce it, read the error, then make one small fix."
        elif any(word in lower for word in ("code", "build", "app")):
            message = "Nice! Break it into a tiny first step, then test it."
        else:
            message = "I heard you. Write the next smallest action and I’ll cheer you on."
        self.say(message)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    CodexPet().run()
