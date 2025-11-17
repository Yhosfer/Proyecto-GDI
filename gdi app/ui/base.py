# ui/base.py
import tkinter as tk
from tkinter import ttk


class BaseModuleFrame(ttk.Frame):
    """Marco base con título y descripción, usado por los módulos de Admin."""
    def __init__(self, parent, title: str, description: str = ""):
        super().__init__(parent, style="Content.TFrame")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        hdr = ttk.Frame(self, style="Content.TFrame")
        hdr.grid(column=0, row=0, sticky="ew", padx=20, pady=(20, 10))
        hdr.columnconfigure(0, weight=1)

        ttk.Label(hdr, text=title, style="Header.TLabel").grid(column=0, row=0, sticky="w")

        if description:
            ttk.Label(
                hdr,
                text=description,
                foreground="#334155",
            ).grid(column=0, row=1, sticky="w", pady=(4, 0))

        self.body = ttk.Frame(self, style="Content.TFrame")
        self.body.grid(column=0, row=1, sticky="nsew", padx=20, pady=10)
