from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image
from pymupdf import Page, Pixmap


def pdf_to_image(pdf_file: Path):
    pdf = fitz.open(pdf_file)
    for page_index in range(len(pdf)):
        page: Page = pdf[page_index]
        print(page.get_text())
        pix: Pixmap = page.get_pixmap(dpi=300)
        img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)  # type: ignore
        img.save(pdf_file.parent / (f'{pdf_file.stem}-{page_index + 1}.jpg'), 'JPEG')
    pdf.close()
    print(pdf_file)
