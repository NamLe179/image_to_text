import tkinter as tk
from tkinter import filedialog, messagebox, Text
from PIL import Image
from pytesseract import pytesseract
import enum
import sys

sys.stdout.reconfigure(encoding='utf-8')

class Language(enum.Enum):
    ENG = 'eng'
    VIE = 'vie'
    ENG_VIE = 'eng+vie'

# Lớp ImageReader cho việc xử lý ảnh và trích xuất văn bản
class ImageReader:
    
    def __init__(self):
        
        windows_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.tesseract_cmd = windows_path
        print('Running\n...................\n')
            
    def extract_text(self, image_path: str, lang: Language) -> str:
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img, lang=lang.value)
        
        # Tách đoạn văn bản
        paragraphs = [p.strip() for p in extracted_text.split('\n\n') if p.strip()]
        return paragraphs

# Hàm để chọn ảnh
def select_image():
    global image_path
    image_path = filedialog.askopenfilename(title="Select an Image",
                                            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        image_label.config(text=f"Selected Image: {image_path}")
    else:
        image_label.config(text="No Image Selected")

# Hàm để thực hiện OCR và hiển thị kết quả
def perform_ocr():
    if not image_path:
        messagebox.showerror("Error", "Please select an image first.")
        return
    
    lang = Language.ENG_VIE  # Đặt ngôn ngữ mặc định là ENG_VIE
    
    try:
        ir = ImageReader()
        paragraphs = ir.extract_text(image_path, lang)
        
        # Hiển thị kết quả trong hộp văn bản
        output_text.delete(1.0, tk.END)
        for i, paragraph in enumerate(paragraphs, start=1):
            processed_text = ' '.join(paragraph.split())
            output_text.insert(tk.END, f"{processed_text}\n\n")
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Giao diện Tkinter
root = tk.Tk()
root.title("Simple OCR App")

# Các biến
image_path = ""

# Nút chọn ảnh
select_btn = tk.Button(root, text="Select Image", command=select_image)
select_btn.pack()

# Nhãn hiển thị ảnh đã chọn
image_label = tk.Label(root, text="No Image Selected")
image_label.pack()

# Nút thực hiện OCR
ocr_btn = tk.Button(root, text="Perform OCR", command=perform_ocr)
ocr_btn.pack()

# Hộp văn bản để hiển thị kết quả OCR
output_text = Text(root, wrap=tk.WORD, width=60, height=20)
output_text.pack()

# Chạy ứng dụng
root.mainloop()
