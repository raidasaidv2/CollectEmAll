import tkinter as tk
from tkinter import ttk
import json
import os

SAVE_FILE = "progress.json"

gwent_cards = [
    {"name": "Ballista", "strength": "6", "ability": "", "source": "Part of the base deck"},
    {"name": "Blue Stripes Commando", "strength": "4", "ability": "Tight Bond: Place next to a card with the same name to double the strength of both cards.",
     "source": "1 purchased from Elsa or Bram in White Orchard\n1 from Crow's Perch quartermaster\n1 from Midcopse's merchant"},
    {"name": "Catapult", "strength": "8", "ability": "Tight Bond: Place next to a card with the same name to double the strength of both cards.",
     "source": "1 from Elsa/Bram in White Orchard\n1 from Marquise Serenity (Passiflora)\n1 from circus camp near Carsten"},
    {"name": "Crinfrid Reavers Dragon Hunter", "strength": "5", "ability": "Tight Bond: Place next to a card with the same name to double the strength of both cards.",
     "source": "1 from Elsa/Bram in White Orchard\n1 from Claywich merchant\n1 from Midcopse merchant"},
    {"name": "Dethmold", "strength": "6", "ability": "", "source": "Part of the base deck"},
    {"name": "Dun Banner Medic", "strength": "5", "ability": "Medic: Choose a discard card to play instantly (not Heroes/Specials).", "source": "Part of the base deck"},
]

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _=None):
        if self.tooltip:
            return
        x, y, *_ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, justify='left',
                         background="#333", foreground="#fff", relief='solid',
                         borderwidth=1, font=("Consolas", 9), wraplength=300)
        label.pack(ipadx=4)

    def hide(self, _=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class GwentTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🃏 Gwent Tracker - Collect 'Em All")
        self.root.geometry("500x600")
        self.root.configure(bg="#1b1b1b")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TCheckbutton", background="#1b1b1b", foreground="#f1c40f", font=("Segoe UI", 10))
        style.configure("TProgressbar", thickness=20, troughcolor="#333", background="#f1c40f")
        style.configure("TLabel", background="#1b1b1b", foreground="#f1c40f", font=("Segoe UI", 14, "bold"))

        self.card_vars = {}
        self.saved_state = self.load_progress()

        ttk.Label(root, text="Gwent Card Tracker").pack(pady=10)
        self.progress = ttk.Progressbar(root, length=400, mode='determinate')
        self.progress.pack(pady=10)

        # Scrollable frame
        canvas = tk.Canvas(root, bg="#1b1b1b", highlightthickness=0)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")

        for card in gwent_cards:
            name = card["name"]
            var = tk.BooleanVar(value=self.saved_state.get(name, False))
            text = f"{name} (Str: {card['strength']})"
            check = ttk.Checkbutton(self.scroll_frame, text=text, variable=var, command=self.update_progress)
            check.pack(anchor="w", pady=3, padx=10)
            tooltip = f"Ability: {card['ability'] or 'None'}\nSource: {card['source']}"
            Tooltip(check, tooltip)
            self.card_vars[name] = var

        self.update_progress()

    def update_progress(self):
        checked = sum(var.get() for var in self.card_vars.values())
        total = len(self.card_vars)
        self.progress['value'] = (checked / total) * 100
        self.save_progress()

    def save_progress(self):
        progress_data = {card: var.get() for card, var in self.card_vars.items()}
        with open(SAVE_FILE, "w") as f:
            json.dump(progress_data, f)

    def load_progress(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        return {}

#Run 
if __name__ == "__main__":
    root = tk.Tk()
    app = GwentTrackerApp(root)
    root.mainloop()
