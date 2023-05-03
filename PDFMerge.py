# merge multiple pdf files into one
import natsort
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import logging

class PDFMerge:
    """
    Merge multiple pdf files into one.
    
    Args:
        folder_path (str): folder path
        do_del_pdf_after_merge (bool): delete original pdf files after merge if True
    """
    def __init__(self,folder_path,do_del_pdf_after_merge=True):
        self.folder_path = folder_path
        self.do_del_pdf_after_merge = do_del_pdf_after_merge
        self.out_folder = os.path.join(folder_path,'merged.pdf')
        logging.info(f'pdf names will be sorted by natsort, so please name your pdf files in order, e.g. p1.pdf, p2.pdf, p3.pdf, ...')
    def merge_pdfs(self,paths,output):
        """Merge pdf files"""
        pdf_writer = PdfFileWriter()
        for path in paths:
            pdf_reader = PdfFileReader(path)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))
        with open(output, 'wb') as out:
            pdf_writer.write(out)

    def del_pdf_after_merge(self,pdf_files):
        """del pdf files after merge"""
        for each in pdf_files:
            os.remove(each)
    
    def __call__(self):
        all_files = os.listdir(self.folder_path)
        pdf_files = [os.path.join(self.folder_path,each) for each in all_files if each.endswith('.pdf')]
        pdf_files = natsort.natsorted(pdf_files)

        self.merge_pdfs(paths = pdf_files, output=self.out_folder)
        if self.do_del_pdf_after_merge:
            self.del_pdf_after_merge(pdf_files)

if __name__ == "__main__":
    folder_path = 'your/dir/pth' # your folder path that contains pdf files
    PDFMerge(folder_path,do_del_pdf_after_merge=False)()