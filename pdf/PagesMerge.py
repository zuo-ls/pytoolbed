# merge multiple pages of a pdf file into one
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2 import PageObject

class PagesMerge:
    """
    merge multiple pages of a pdf file into one long page.

    Args:
        path: the path of the pdf file. eg: 'XXX.pdf'
    """
    def __init__(self,path):
        self.path = path
    def __call__(self,):
        reader = PdfFileReader(open(self.path,'rb'))
        writer = PdfFileWriter()
        number_of_pages = reader.getNumPages()
        page_1 = reader.getPage(0)
        heights = [int(page_1.mediaBox.getHeight()*i) for i in range(number_of_pages)]
        heights.reverse()

        page = PageObject.createBlankPage(None,page_1.mediaBox.getWidth(),page_1.mediaBox.getHeight()*number_of_pages)
        for i in range(number_of_pages):
            page.mergeScaledTranslatedPage(reader.getPage(i), 1, 0, heights[i])

        writer.addPage(page)
        with open(self.path.split('.')[0]+'_out.pdf', 'wb') as f:
            writer.write(f)

if __name__ == '__main__':
    path = 'XXX.pdf'
    PagesMerge(path)()
        