import os

def get_file_extension(file_path):
    return os.path.splitext(file_path)[1].lower()

def is_image_file(file_path):
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'}
    return get_file_extension(file_path) in image_extensions

def is_pdf_file(file_path):
    return get_file_extension(file_path) == '.pdf'