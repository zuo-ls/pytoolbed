# pytoolbed

Simplify your work using python-based tool.

## currently support tools

### 1 pdf tools

* MarginAdd: Add margins to your PDF file(s).
* PagesMerge: Merge multiple pages of a PDF file into one long page.
* PDFMerge: Merge multiple PDF files into one.
* image2pdf

### 2 tex-eq

handle your math equations.

directly use notebooks, which can read from and paste contents to the clipboard.

- OCR: read image to latex.

  - read your img of equations saving in your clipboard and generate latex str, the outputs will auto save in your clipboard, therefore you can directly paste.
- tex to mathml for word.

  - read latex str and change it to mathml, which auto saved in clipboard, the output can be directly paste into a word file.
- latex str to image for PPT.

  - generate png given latex string/read it from clipboard, the png is saved in clipboard, you can just paste.

### 3 id fig watermark

A powerful Python tool for adding secure, verifiable watermarks to images, particularly designed for identity documents and sensitive images.

给身份证打码用的，图片模糊 + 水印 + 一个独有编码。(代码由 AI 辅助生成。)

### -1 others
image reducer: resize_image according to the journels' requirements.