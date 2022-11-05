import os
import PyPDF2 as pdf
import uuid


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def rotate_pages(file: str, angle: int, pages: list[int]):
    with open(file, 'rb') as f:
        pdf_reader = pdf.PdfFileReader(f)
        pdf_writer = pdf.PdfFileWriter()
        for page in range(pdf_reader.getNumPages()):
            fpage = pdf_reader.getPage(page)
            if str(page + 1) in pages:
                fpage.rotateClockwise(int(angle))
            pdf_writer.addPage(fpage)

        file_out_name = str(uuid.uuid4()) + '.pdf'
        with open(os.path.join(MEDIA_ROOT, file_out_name), 'wb') as f:
            pdf_writer.write(f)
            return file_out_name