import threading
import os
import platform
import subprocess
from tkinter import messagebox
from pypdf import PdfWriter

from .pdf_processor import process_pdf_file
from .image_processor import process_image_file

class PdfConverter:
    def __init__(self):
        pass
        
    def start_conversion(self, image_paths, pdf_paths, output_path, pdf_pages_dict, 
                       progress_callback, done_callback, error_callback):
        thread = threading.Thread(
            target=self._convert_worker, 
            args=(image_paths, pdf_paths, output_path, pdf_pages_dict, 
                 progress_callback, done_callback, error_callback),
            daemon=True
        )
        thread.start()
    
    def _convert_worker(self, image_paths, pdf_paths, output_path, pdf_pages_dict,
                      progress_callback, done_callback, error_callback):
        try:
            writer = PdfWriter()
            total_files = len(image_paths) + len(pdf_paths)
            processed = 0
            
            # Process images
            for img_path in image_paths:
                process_image_file(img_path, writer)
                processed += 1
                progress_callback(processed / total_files * 100)
            
            # Process PDFs
            for pdf_path in pdf_paths:
                process_pdf_file(pdf_path, writer, pdf_pages_dict)
                processed += 1
                progress_callback(processed / total_files * 100)
            
            # Write output
            with open(output_path, "wb") as fp:
                writer.write(fp)
            
            done_callback(output_path)
            self._open_output_folder(output_path)
            
        except Exception as e:
            error_callback(e)
    
    def _open_output_folder(self, output_path):
        try:
            folder = os.path.dirname(os.path.abspath(output_path))
            if platform.system() == 'Windows':
                os.startfile(folder)
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', folder])
            else:
                subprocess.Popen(['xdg-open', folder])
        except Exception:
            pass