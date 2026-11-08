from pathlib import Path

import pymupdf

pdf = list(Path("sample_resumes").glob("*.pdf"))[0]
source = pymupdf.open(pdf)


pix = source[0].get_pixmap(dpi=100)


out = pymupdf.open()
page = out.new_page(width=pix.width, height=pix.height)
page.insert_image(page.rect, pixmap=pix)
out.save("sample_resumes/other/scanned_test.pdf")

print("Saved sample_resumes/other/scanned_test.pdf")