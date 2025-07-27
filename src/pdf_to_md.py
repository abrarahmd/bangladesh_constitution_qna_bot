import pdfplumber
from markdownify import markdownify as md
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text

def convert_pdf_to_md(pdf_path, output_md_path):
    raw_text = extract_text_from_pdf(pdf_path)
    markdown_text = md(raw_text)
    os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
    
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    print(f"✅ Markdown saved to {output_md_path}")

if __name__ == "__main__":
    convert_pdf_to_md("data/raw_pdfs/bangladesh_constitution.pdf", "data/pdf_markdown/constitution.md")
