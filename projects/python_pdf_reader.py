from pathlib import Path

from pypdf import PdfReader


def read_content(path: Path):
    with PdfReader(path) as reader:
        print(len(reader.pages))
        txt = reader.pages[0].extract_text()
        print(txt)
        reader.close()
    # time.sleep(1)
