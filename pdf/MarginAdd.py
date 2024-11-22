from PyPDF2 import PdfFileReader, PdfFileWriter
from tqdm import tqdm
import os

class MarginAdd:
    """
    add margin to pdf file(s).

    Args:
    - margin_w: margin width
    - margin_h: margin height
    - addblankpage: list. for example, [0,1] will add blank page before page 0 and page 1.
    """
    def __init__(self,margin_w=120,margin_h=0,addblankpage=None):
        self.margin_w = margin_w
        self.margin_h = margin_h
        self.addblankpage = addblankpage
    def add_margin(self,path,outpath,margin_w,margin_h,addblankpage=None):
        """
        modify from https://gist.github.com/polonez/1fc01988935607b57f6ddcd7753acc7a
        """
        with open(path, 'rb') as f:
            p = PdfFileReader(f)
            info = p.getDocumentInfo()
            number_of_pages = p.getNumPages()
            writer = PdfFileWriter()
            print(f'margin_w: {margin_w}\nmargin_h:{margin_h}')
            for i in tqdm(range(number_of_pages)):
                page = p.getPage(i)
                if addblankpage != None and i in addblankpage:
                    writer.addBlankPage(
                        page.mediaBox.getWidth() + 2 * margin_w,
                        page.mediaBox.getHeight() + 2 * margin_h
                    )
                new_page = writer.addBlankPage(
                    page.mediaBox.getWidth() + 2 * margin_w,
                    page.mediaBox.getHeight() + 2 * margin_h
                )
                new_page.mergeScaledTranslatedPage(page, 1, margin_w, margin_h)
            with open(outpath, 'wb') as f:
                writer.write(f)
    def process_single_file(self,path):
        out_path = path.split('.')[0]+'_out.pdf'
        self.add_margin(path,out_path,self.margin_w,self.margin_h,self.addblankpage)
    def process_multi_files(self,dir_path):
        out_folder = os.path.join(dir_path,'out')
        os.makedirs(out_folder)
        pdf_files = os.listdir(dir_path)
        for each in pdf_files:
            if each.endswith('pdf'):
                in_path = os.path.join(dir_path,each)
                out_path = os.path.join(out_folder,each)
                print('dealing with {}'.format(each))
                self.add_margin(in_path,out_path,self.margin_w,self.margin_h,self.addblankpage)
        print('done!')

if __name__ == '__main__':
    marginadder = MarginAdd(margin_w=120,margin_h=0,addblankpage=[0])
    # try the following to add margin to a single file
    marginadder.process_single_file('XXX.pdf')
    # try the following to add margin to all pdf files in a folder
    marginadder.process_multi_files('your/path/to/folder/pdfs')
