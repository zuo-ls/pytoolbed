# BibTeX to BBL Converter

A simple command-line tool to convert BibTeX (.bib) files to BBL format.

## Installation

1. Ensure Python is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Convert a BibTeX file to BBL:
```bash
python bib2bbl.py input_file=new.bib output_file=new.bbl
```

## Features

- Converts BibTeX entries to BBL format
- Maintains proper formatting for authors, titles, and journals
- Automatically sorts entries by citation key
- Supports UTF-8 encoding

## Example

Input BibTeX:
```bibtex
@article{smith2020example,
    author = {Smith, John and Doe, Jane},
    title = {An Example Paper},
    journal = {Journal of Examples},
    year = {2020},
    volume = {1},
    number = {2},
    pages = {34--56}
}
```

Output BBL:
```latex
\begin{thebibliography}{99}

\bibitem{smith2020example} Smith, John and Doe, Jane. An Example Paper. \textit{Journal of Examples} 1(2):34--56 (2020).

\end{thebibliography}
``` 