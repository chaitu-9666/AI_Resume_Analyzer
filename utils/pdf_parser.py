from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(file):
    # Ensure file pointer is at the beginning
    file.seek(0)
    
    # Read file content into memory for better compatibility
    file_content = file.read()
    file_like = io.BytesIO(file_content)
    
    reader = PdfReader(file_like)
    text = ""

    for page in reader.pages:
        try:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        except Exception:
            # Skip pages that can't be read
            continue

    return text.strip()
