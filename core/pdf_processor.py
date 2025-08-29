import os
from pypdf import PdfReader
from pdf2image import convert_from_path

def process_pdf_file(pdf_path, writer, pdf_pages_dict):
    if pdf_path in pdf_pages_dict and pdf_pages_dict[pdf_path]:
        # Use modified pages
        pages = pdf_pages_dict[pdf_path]
        for p in pages:
            tmp_path = pdf_path + "_temp_page.pdf"
            p.save(tmp_path, "PDF")
            reader = PdfReader(tmp_path)
            for page in reader.pages:
                writer.add_page(page)
            os.remove(tmp_path)
    else:
        # Use original PDF
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            writer.add_page(page)