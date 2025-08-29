import os
from PIL import Image, ImageOps, ImageTk
from pdf2image import convert_from_path
from tkinter import ttk

class PreviewManager:
    def __init__(self, parent_component):
        self.parent = parent_component
        self._thumbnail_ref = None

        # PDF previews
        self.pdf_preview_images = []
        self.pdf_preview_index = 0
        self.pdf_pages_dict = {}
        self.current_pdf_path = None

        # Image previews
        self.image_preview_list = []
        self.image_preview_index = 0

        # Mode
        self.preview_mode = None  # "pdf" or "image"

    def apply_theme(self, bg_color, fg_color):
        self.preview_box.configure(background=bg_color, foreground=fg_color)

    def setup_preview_ui(self, parent_frame):
        preview_lbl = ttk.Label(parent_frame, text='Preview')
        preview_lbl.pack(anchor='nw')

        self.preview_box = ttk.Label(parent_frame, text='No file selected',
                                     relief='sunken', anchor='center')
        self.preview_box.pack(pady=6, ipadx=6, ipady=6, fill='both', expand=True)

        # PDF navigation 
        self.nav_frame = ttk.Frame(parent_frame)
        self.prev_btn = ttk.Button(self.nav_frame, text="◀ Prev", command=self.prev_page)
        self.next_btn = ttk.Button(self.nav_frame, text="Next ▶", command=self.next_page)
        self.del_btn = ttk.Button(self.nav_frame, text="🗑 Delete Page", command=self.delete_page)

        self.prev_btn.pack(side="left", padx=2)
        self.next_btn.pack(side="left", padx=2)
        self.del_btn.pack(side="left", padx=2)

        # نبدأ مخفي
        self.nav_frame.pack_forget()

    def show_image_preview(self, image_path):
        try:
            self.preview_mode = "image"
            # اخفي أزرار الـ PDF
            self.nav_frame.pack_forget()

            if image_path not in self.image_preview_list:
                self.image_preview_list.append(image_path)
            self.image_preview_index = self.image_preview_list.index(image_path)

            self._show_image_page()
        except Exception:
            self.preview_box.config(text="Cannot preview image")

    def _show_image_page(self):
        if not self.image_preview_list:
            self.preview_box.config(text="No images")
            return
        img_path = self.image_preview_list[self.image_preview_index]
        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)
        img.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(img)
        self.preview_box.config(image=photo,
                                text=f"Image {self.image_preview_index+1}/{len(self.image_preview_list)}")
        self._thumbnail_ref = photo

    def show_pdf_preview(self, pdf_path):
        try:
            self.preview_mode = "pdf"
            self.current_pdf_path = pdf_path
            # أظهر أزرار التنقل
            self.nav_frame.pack(pady=4)

            if pdf_path in self.pdf_pages_dict:
                pages = self.pdf_pages_dict[pdf_path]
            else:
                pages = convert_from_path(pdf_path, dpi=80)
                self.pdf_pages_dict[pdf_path] = pages

            self.pdf_preview_images = pages
            self.pdf_preview_index = 0
            self._show_pdf_page()
        except Exception as e:
            self.preview_box.config(text=f"Cannot preview PDF: {e}")

    def _show_pdf_page(self):
        if not self.pdf_preview_images:
            self.preview_box.config(text="No PDF pages")
            return
        img = self.pdf_preview_images[self.pdf_preview_index]
        img.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(img)
        self.preview_box.config(image=photo,
                                text=f"Page {self.pdf_preview_index+1}/{len(self.pdf_preview_images)}")
        self._thumbnail_ref = photo

    def next_page(self):
        if self.preview_mode == "pdf":
            if self.pdf_preview_images and self.pdf_preview_index < len(self.pdf_preview_images) - 1:
                self.pdf_preview_index += 1
                self._show_pdf_page()

    def prev_page(self):
        if self.preview_mode == "pdf":
            if self.pdf_preview_images and self.pdf_preview_index > 0:
                self.pdf_preview_index -= 1
                self._show_pdf_page()

    def delete_page(self):
        if self.preview_mode == "pdf":
            if not self.current_pdf_path or not self.pdf_preview_images:
                return
            if len(self.pdf_preview_images) == 0:
                return

            del self.pdf_preview_images[self.pdf_preview_index]
            self.pdf_pages_dict[self.current_pdf_path] = self.pdf_preview_images

            if not self.pdf_preview_images:
                self.preview_box.config(text="No pages left in PDF")
                return

            if self.pdf_preview_index >= len(self.pdf_preview_images):
                self.pdf_preview_index = len(self.pdf_preview_images) - 1

            self._show_pdf_page()

    def clear_preview(self):
        self.preview_box.config(image='', text='No file selected')
        self._thumbnail_ref = None
        self.nav_frame.pack_forget()
