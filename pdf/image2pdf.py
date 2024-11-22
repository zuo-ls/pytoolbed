from PIL import Image
import os
from PyPDF2 import PdfFileWriter

def image_to_pdf(images_dir, out_pth):
    images = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.PNG')]
    images.sort()
    print(images)
    pdf_writer = PdfFileWriter()
    for image in images:
        img = Image.open(image)
        img = img.convert('RGB')
        save_pth = os.path.join(images_dir, image.split('/')[-1].split('.')[0] + '.pdf')
        img.save(save_pth, 'PDF', resolution=100.0)
        pdf_writer.add_page(PdfFileReader(save_pth).getPage(0))
        os.remove(save_pth)

    with open(out_pth, 'wb') as out:
        pdf_writer.write(out)

# Example
# images_dir = 'pth/to/images/'
# out_pth = images_dir + 'out.pdf'
# image_to_pdf(images_dir, out_pth)