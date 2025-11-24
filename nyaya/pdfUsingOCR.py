import platform
from pathlib import Path
import pytesseract
try:
    import fitz 
except ImportError:
    print("PyMuPDF not found. Install it with: pip install PyMuPDF")
    exit(1)
from PIL import Image
import io

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    out_directory = Path("E:/Shashank SinghNyaya/logs").expanduser()
else:
    out_directory = Path("~").expanduser()

PDF_file = Path("E:/Shashank Singh/Nyaya/dataset/fir/fir1.pdf")
text_file = out_directory / Path("pdfTextExtractor.txt")

def main():
    if not PDF_file.exists():
        print(f"Error: PDF file '{PDF_file}' not found!")
        return
    
    try:
        pdf_document = fitz.open(PDF_file)
        page_count = len(pdf_document)
        print(f"Converting {page_count} pages...")
        
        with open(text_file, "w", encoding='utf-8') as output_file:
            for page_num in range(page_count):
                print(f"Processing page {page_num + 1}/{page_count}")
                
                page = pdf_document[page_num]
                
                mat = fitz.Matrix(2.0, 2.0)  
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                
                image = Image.open(io.BytesIO(img_data))
                
                # Run OCR
                text = pytesseract.image_to_string(image)
                text = text.replace("-\n", "")
                
                # Write to file
                output_file.write(f"--- Page {page_num + 1} ---\n")
                output_file.write(text + "\n\n")
        
        pdf_document.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()