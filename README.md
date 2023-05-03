# PDFProcess

This repository contains several files to help you process your PDF files. You can use the following functionalities:

1. MarginAdd: Add margins to your PDF file(s).
2. PagesMerge: Merge multiple pages of a PDF file into one long page.
3. PDFMerge: Merge multiple PDF files into one.

一些自用的pdf处理脚本, 现在支持的功能包括: 

1. MarginAdd: 给PDF上下左右添加空白边距方便笔记.
2. PagesMerge: 将多页pdf合并成一个长页.
3. PDFMerge: 将多个PDF文件合并成一个文件.

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