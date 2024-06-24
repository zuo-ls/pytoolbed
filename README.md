# PDFProcess

This repository contains several files to help you process your PDF files. You can use the following functionalities:

1. MarginAdd: Add margins to your PDF file(s).
2. PagesMerge: Merge multiple pages of a PDF file into one long page.
3. PDFMerge: Merge multiple PDF files into one.
4. image2pdf

### Dependency

```python
pypdf2 2.2.0 
```

### Usage

1. Add margin to pdf file(s).

   ```python
   marginadder = MarginAdd(margin_w=120,margin_h=0,addblankpage=[0])
   
   # try the following to add margin to a single file
   marginadder.process_single_file('XXX.pdf')
   
   # try the following to add margin to all pdf files in a folder
   marginadder.process_multi_files('your/path/to/pdfs/folder')
   ```

2. Merge multiple pages of a pdf file into one long page.

   ```python
   path = 'XXX.pdf'
   PagesMerge(path)()
   ```

3. Merge multiple pdf files into one.

   ```python
   folder_path = 'your/dir/pth' # your folder path that contains pdf files
   PDFMerge(folder_path,do_del_pdf_after_merge=False)()
   ```

4. Merge multiple images into one pdf.
   ```python
   images_dir = 'pth/to/images/'
   out_pth = images_dir + 'out.pdf'
   image_to_pdf(images_dir, out_pth)
   ```