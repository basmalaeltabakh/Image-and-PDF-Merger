import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
from reportlab.lib.pagesizes import letter, A4, legal

from core.converter import PdfConverter
from utils.preview_utils import PreviewManager
from .themes import ThemeManager
from tkinterdnd2 import DND_FILES

PAGE_SIZES = {
    "Letter (8.5x11 in)": letter,
    "A4 (210x297 mm)": A4,
    "Legal (8.5x14 in)": legal
}

class ImageToPdfConverter(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.image_paths = []
        self.pdf_paths = []
        self.output_pdf_path = tk.StringVar(value="")
        
        self.theme_manager = ThemeManager(self.parent)
        self.preview_manager = PreviewManager(self)
        self.converter = PdfConverter()
        
        self.page_size = tk.StringVar(value="Letter (8.5x11 in)")

        self._build_ui()
        

    def _build_ui(self):
        self.theme_manager.apply_theme()
        

        header = ttk.Label(self.parent, text="Image & PDF Merger", style='Header.TLabel')
        header.pack(padx=10, pady=(10, 6))

        toolbar = ttk.Frame(self.parent)
        toolbar.pack(fill='x', padx=10, pady=6)

        self._create_toolbar_buttons(toolbar)
        self._create_main_content()

    def _create_toolbar_buttons(self, toolbar):
        self.add_btn = ttk.Button(toolbar, text='Add Images', command=self.add_images, style="Custom.TButton")

        self.add_btn.pack(side='left')

        self.add_pdf_btn = ttk.Button(toolbar, text='Add PDF', command=self.add_pdf,style="Custom.TButton")
        self.add_pdf_btn.pack(side='left', padx=(6, 0))

        self.remove_btn = ttk.Button(toolbar, text='Remove Selected', command=self.remove_selected,style="Custom.TButton")
        self.remove_btn.pack(side='left', padx=(6, 0))

        self.up_btn = ttk.Button(toolbar, text='Move Up', command=self.move_up,style="Custom.TButton")
        self.up_btn.pack(side='left', padx=(6, 0))

        self.down_btn = ttk.Button(toolbar, text='Move Down', command=self.move_down,style="Custom.TButton")
        self.down_btn.pack(side='left', padx=(6, 0))

        theme_btn = ttk.Button(toolbar, text="Toggle Theme", command=self.toggle_theme,style="Custom.TButton")
        theme_btn.pack(side='left', padx=(6, 0))

        spacer = ttk.Label(toolbar, text='')
        spacer.pack(side='left', expand=True)

        self.page_size_combo = ttk.Combobox(toolbar, textvariable=self.page_size, 
                                          values=list(PAGE_SIZES.keys()), state="readonly")
        self.page_size_combo.pack(side='left', padx=(0, 6))

        self.saveas_btn = ttk.Button(toolbar, text='Choose output...', command=self.browse_save)
        self.saveas_btn.pack(side='left', padx=(0, 6))

        self.convert_btn = ttk.Button(toolbar, text='Convert to PDF', command=self.start_conversion)
        self.convert_btn.pack(side='left')

    def _create_main_content(self):
        main = ttk.Frame(self.parent)
        main.pack(fill='both', expand=True, padx=10, pady=6)

        left = ttk.Frame(main)
        left.pack(side='left', fill='both', expand=True)

        self.listbox = tk.Listbox(left, selectmode=tk.SINGLE, activestyle='dotbox')
        self.listbox.pack(side='left', fill='both', expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        # Drag & Drop
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.on_drop)

        lb_scroll = ttk.Scrollbar(left, orient='vertical', command=self.listbox.yview)
        lb_scroll.pack(side='left', fill='y')
        self.listbox.config(yscrollcommand=lb_scroll.set)

        right = ttk.Frame(main, width=320)
        right.pack(side='right', fill='y', padx=(10, 0))

        self.preview_manager.setup_preview_ui(right)

        out_label = ttk.Label(right, text='Output file:')
        out_label.pack(anchor='w', pady=(10, 0))

        self.out_entry = ttk.Entry(right, textvariable=self.output_pdf_path, width=40)
        self.out_entry.pack(fill='x', pady=(2, 6))

        self.progress = ttk.Progressbar(right, orient='horizontal', mode='determinate', maximum=100)
        self.progress.pack(fill='x', pady=(8, 0))

    # ----------------- UI actions -----------------
    def on_drop(self, event):
        files = self.parent.tk.splitlist(event.data)
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")):
                if f not in self.image_paths:
                    self.image_paths.append(f)
            elif f.lower().endswith(".pdf"):
                if f not in self.pdf_paths:
                    self.pdf_paths.append(f)
        self._update_listbox()

    def add_images(self):
        paths = filedialog.askopenfilenames(title='Select images',
                                            filetypes=[('Image files', '*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.gif')])
        for p in paths:
            if p not in self.image_paths:
                self.image_paths.append(p)
        self._update_listbox()

    def add_pdf(self):
        paths = filedialog.askopenfilenames(title='Select PDFs', filetypes=[('PDF files', '*.pdf')])
        for p in paths:
            if p not in self.pdf_paths:
                self.pdf_paths.append(p)
        self._update_listbox()

    def remove_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        item = self.listbox.get(idx)
        if item.endswith("[PDF]"):
            self.pdf_paths.pop(idx - len(self.image_paths))
        else:
            self.image_paths.pop(idx)
        self._update_listbox()
        self.preview_manager.clear_preview()

    def move_up(self):
        sel = self.listbox.curselection()
        if not sel or sel[0] == 0:
            return
        idx = sel[0]
        self._swap_items(idx, idx - 1)
        self._update_listbox()
        self.listbox.selection_set(idx - 1)

    def move_down(self):
        sel = self.listbox.curselection()
        if not sel or sel[0] == self.listbox.size() - 1:
            return
        idx = sel[0]
        self._swap_items(idx, idx + 1)
        self._update_listbox()
        self.listbox.selection_set(idx + 1)

    def _swap_items(self, i, j):
        items = self.image_paths + self.pdf_paths
        items[i], items[j] = items[j], items[i]
        self.image_paths = [x for x in items if x.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif"))]
        self.pdf_paths = [x for x in items if x.lower().endswith(".pdf")]

    def browse_save(self):
        default_name = 'output.pdf'
        path = filedialog.asksaveasfilename(defaultextension='.pdf',
                                            filetypes=[('PDF file', '*.pdf')],
                                            initialfile=default_name)
        if path:
            self.output_pdf_path.set(path)

    def on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        item = self.listbox.get(idx)

        if item.endswith("[PDF]"):
            self.preview_manager.show_pdf_preview(self.pdf_paths[idx - len(self.image_paths)])
        else:
            self.preview_manager.show_image_preview(self.image_paths[idx])

    def _update_listbox(self):
        self.listbox.delete(0, tk.END)
        for p in self.image_paths:
            self.listbox.insert(tk.END, os.path.basename(p))
        for p in self.pdf_paths:
            self.listbox.insert(tk.END, os.path.basename(p) + " [PDF]")

    # ----------------- Conversion -----------------
    def start_conversion(self):
        if not (self.image_paths or self.pdf_paths):
            messagebox.showerror('Error', 'No files to convert')
            return
        out = self.output_pdf_path.get().strip()
        if not out:
            self.browse_save()
            out = self.output_pdf_path.get().strip()
            if not out:
                return

        self._set_controls_state('disabled')
        self.progress['value'] = 0

        self.converter.start_conversion(
            self.image_paths,
            self.pdf_paths,
            out,
            self.preview_manager.pdf_pages_dict,
            self._on_conversion_progress,
            self._on_conversion_done,
            self._on_conversion_error
        )

    def _set_controls_state(self, state='normal'):
        for w in (self.add_btn, self.add_pdf_btn, self.remove_btn, self.up_btn,
                  self.down_btn, self.saveas_btn, self.convert_btn):
            w.config(state=state)

    def _on_conversion_progress(self, value):
        self.progress['value'] = value

    def _on_conversion_done(self, out_path):
        self.progress['value'] = 100
        messagebox.showinfo('Success', f'PDF saved as:\n{out_path}')
        self._set_controls_state('normal')

    def _on_conversion_error(self, error):
        messagebox.showerror('Error', str(error))
        self._set_controls_state('normal')

    # ----------------- Theme -----------------
    
    def toggle_theme(self):
        self.theme_manager.toggle_theme()
         
    
    