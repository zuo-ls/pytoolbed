import PyPDF2

def remove_annotations(pdf_path):
    """Remove annotations from a PDF file."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        writer = PyPDF2.PdfFileWriter()

        # Iterate through each page and remove annotations
        for i in range(reader.getNumPages()):
            page = reader.getPage(i)
            if '/Annots' in page:
                page[PyPDF2.generic.NameObject('/Annots')] = PyPDF2.generic.ArrayObject()

            writer.addPage(page)
        
        output_path = pdf_path.split('.')[0]+'_out.pdf'

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

if __name__ == '__main__':
    remove_annotations('sample.pdf')