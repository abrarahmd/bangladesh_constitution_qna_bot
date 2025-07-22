import pdfplumber
from typing import Optional, List

def extract_text(
    pdf_path: str,
    start_page: Optional[int] = None,
    end_page: Optional[int] = None,
    warn: bool = True,
    return_pages: bool = False
) -> str | List[str]:

    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        if start_page or end_page:
            pages = pages[(start_page-1 if start_page else 0):(end_page if end_page else None)]
        
        for idx, page in enumerate(pages, (start_page or 1)):
            page_text = page.extract_text()
            if page_text:
                texts.append(page_text)
            elif warn:
                print(f"[Warning] Page {idx} is blank or contains no extractable text.")
    
    if not texts:
        raise ValueError(f"No text could be extracted from {pdf_path}. Is it a scanned/image-based PDF?")
    
    if return_pages:
        return texts
    return "\n\n".join(texts)
