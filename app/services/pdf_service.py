import fitz
from PIL import Image
import io


def pdf_to_images(pdf_bytes):

    images = []

    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page in pdf:

        pix = page.get_pixmap()

        img_bytes = pix.tobytes("png")

        image = Image.open(io.BytesIO(img_bytes))

        images.append(image)

    return images