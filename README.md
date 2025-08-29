# 📄 PDF & Image Merger Desktop Application

This project is a **PDF and Image Merger Desktop Application** built using Python's **Tkinter** library.  
It allows users to combine multiple image files (`PNG, JPG, JPEG, BMP, TIFF, GIF`) and PDF documents into a single PDF file.  
The application also provides features for previewing files, reordering them, and deleting pages from PDFs before conversion.  

👉 The project has been packaged as a **Desktop Application using PyInstaller**, and a **DesktopApp.rar file** is uploaded in the repository.  
Anyone can simply download and run it without needing to install Python or dependencies.   

---

## ✨ Features

- **Merge Images and PDFs**  
  - Combine various image formats and PDF files into one consolidated PDF document.

- **File Management**  
  - Add images and PDFs through file dialogs or drag-and-drop.  
  - Remove selected files from the list.  
  - Reorder files using **Move Up** and **Move Down** buttons.  

- **File Preview**  
  - View previews of selected image files.  
  - Preview PDF documents page by page with navigation controls (**Previous, Next**).  
  - Delete individual pages from PDF previews.  

- **Customizable Output**  
  - Choose the output PDF file path.  
  - Select standard page sizes (**Letter, A4, Legal**) for the output PDF.  

- **Progress Tracking**  
  - Monitor the conversion progress with a progress bar.  

- **Theming**  
  - Toggle between **light** and **dark** themes.  

- **Desktop Application**  
  - Available as a **standalone executable** via **PyInstaller**.  
  - Users can download the **DesktopApp.rar file** from the repository, extract it, and run the app directly.  

---

## 🛠️ Technologies Used

- **Python 3**  
- **Tkinter** → Graphical User Interface  
- **Pillow (PIL)** → Image processing  
- **pdf2image** → Convert PDF pages to images for preview  
- **PyPDF** → Merge & manipulate PDFs  
- **tkinterdnd2** → Drag-and-drop functionality  
- **reportlab** → Standard page sizes  
- **PyInstaller** → Build executable desktop app  

---

## ▶️ Usage

### 🔹 Run the prebuilt Desktop Application
1. Download the `.rar` file from this repository.  
2. Extract it.  
3. Run the `.exe` file inside the folder. ✅  

👉 **No Python installation required!**

---

## 📥 Add Files
- Click **"Add Images"** to select image files.  
- Click **"Add PDF"** to select PDF files.  
- Drag & drop image/PDF files directly into the listbox.  

---

## 🗂️ Manage Files
- Select a file in the listbox to preview it.  
- Use **Remove Selected** to delete a file.  
- Use **Move Up / Move Down** to reorder files.  
- For PDFs → use **Prev, Next, Delete Page** to navigate/modify pages.  

---

## 📑 Choose Output
- Click **"Choose output..."** to specify the output PDF file path.  
- Select page size from dropdown (**Letter, A4, Legal**).  

---

## ⚡ Convert
- Click **"Convert to PDF"** → progress bar shows merging progress.  

---

## 🎨 Toggle Theme
- Switch between **light** and **dark** modes.  

---

## 📂 Project Structure
```
.
├── main.py                     # Main application entry point
├── gui/                        # GUI related modules
│   ├── __init__.py
│   ├── components.py           # Main application frame (ImageToPdfConverter)
│   ├── main_window.py          # Main Tkinter window setup
│   ├── themes.py               # Theme management logic
│   └── themes.json             # Theme color definitions
├── core/                       # Core logic for PDF/Image processing
│   ├── __init__.py
│   ├── converter.py            # Conversion process (threading, file handling)
│   ├── image_processor.py      # Converts images to temporary PDFs
│   └── pdf_processor.py        # Processes PDF files for merging
└── utils/                      # Utility functions
    ├── __init__.py
    ├── file_utils.py           # File extension utilities
    └── preview_utils.py        # Manages image & PDF previews
```

