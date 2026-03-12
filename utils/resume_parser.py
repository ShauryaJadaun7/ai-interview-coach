import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract clean text from uploaded PDF resume.
    Handles any resume format reliably.
    """
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text")
        return text.strip()
    except Exception as e:
        raise ValueError(f"PDF parsing failed: {str(e)}")