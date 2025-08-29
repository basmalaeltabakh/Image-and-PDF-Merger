import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self, parent):
        self.parent = parent
        self.current_theme = "light"
        
    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()
        
    def apply_theme(self):
        style = ttk.Style(self.parent)
        style.theme_use('clam')  # Use clam theme for better styling control

        if self.current_theme == "light":
            bg_main = "#ffffff"
            fg_text = "#000000"
            btn_bg = "#f0f0f0"
            btn_fg = "#000000"
            border_color = "#cccccc"
        else:
            bg_main = "#000000"
            fg_text = "#ffffff"
            btn_bg = "#000000"  # pure black for buttons
            btn_fg = "#ffffff"
            border_color = "#444444"

        self.parent.configure(bg=bg_main)

        style.configure('.', background=bg_main, foreground=fg_text, font=('Segoe UI', 10))

        style.configure('Header.TLabel',
                    font=('Segoe UI', 16, 'bold'),
                    background=bg_main, foreground=fg_text)

        style.configure('TButton',
        font=('Segoe UI', 9, 'bold'),
        padding=(10, 5),
        background=btn_bg,
        foreground=btn_fg,
        borderwidth=1,
        relief="solid"
    )

        style.map('TButton',
        background=[('active', '#222222'), ('pressed', '#111111'), ('!disabled', btn_bg)],
        foreground=[('active', btn_fg), ('pressed', btn_fg), ('!disabled', btn_fg)]
    )

        style.configure('TEntry', fieldbackground=bg_main, foreground=fg_text)
        style.configure('TCombobox', fieldbackground=bg_main, foreground=fg_text)
        style.configure('TProgressbar', background=fg_text)

        self._update_widgets(self.parent, bg_main, fg_text, border_color)

    def _update_widgets(self, parent, bg_main, fg_text, border_color):
        for widget in parent.winfo_children():
            if isinstance(widget, tk.Listbox):
                widget.configure(bg=bg_main, fg=fg_text,
                                 selectbackground=fg_text, selectforeground=bg_main,
                                 highlightbackground=border_color, highlightcolor=border_color,
                                 highlightthickness=1)
            elif isinstance(widget, (tk.Text, tk.Canvas)):
                widget.configure(bg=bg_main, fg=fg_text,
                                 highlightbackground=border_color, highlightcolor=border_color,
                                 highlightthickness=1)
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=bg_main,
                                 highlightbackground=border_color, highlightcolor=border_color,
                                 highlightthickness=1)
            elif isinstance(widget, tk.Button):
                widget.configure(bg=btn_bg, fg=btn_fg,
                                 highlightbackground=border_color, highlightcolor=border_color,
                                 highlightthickness=1)

            if hasattr(widget, 'winfo_children') and widget.winfo_children():
                self._update_widgets(widget, bg_main, fg_text, border_color)

