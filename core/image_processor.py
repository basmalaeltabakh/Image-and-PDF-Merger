import os
from PIL import Image, ImageOps
from pypdf import PdfReader

def process_image_file(image_path, writer):
    pil_img = Image.open(image_path)
    pil_img = ImageOps.exif_transpose(pil_img).convert('RGB')
    tmp_path = image_path + "_temp_page.pdf"
    pil_img.save(tmp_path, "PDF")
    reader = PdfReader(tmp_path)
    for page in reader.pages:
        writer.add_page(page)
    os.remove(tmp_path)