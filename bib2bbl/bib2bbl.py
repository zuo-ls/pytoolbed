import click
from pybtex.database.input import bibtex
import os
from omegaconf import OmegaConf

def format_bbl_entry(entry):
    """Format a single bibliography entry in BBL format."""
    authors = ' and '.join(str(person) for person in entry.persons.get('author', []))
    title = entry.fields.get('title', '')
    year = entry.fields.get('year', '')
    journal = entry.fields.get('journal', '')
    volume = entry.fields.get('volume', '')
    number = entry.fields.get('number', '')
    pages = entry.fields.get('pages', '')
    
    bbl = []
    bbl.append(r'\bibitem{' + entry.key + '}')
    if authors:
        bbl.append(authors + '.')
    if title:
        bbl.append(' ' + title + '.')
    if journal:
        bbl.append(' \\textit{' + journal + '}')
        if volume:
            bbl.append(' ' + volume)
            if number:
                bbl.append('(' + number + ')')
        if pages:
            bbl.append(':' + pages)
    if year:
        bbl.append(' (' + year + ').')
    
    return ' '.join(bbl)

def convert(input_file, output_file=None):
    """Convert BibTeX (.bib) file to BBL format."""
    # If output file is not specified, create it with the same name but .bbl extension
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.bbl'
    
    # Parse the BibTeX file
    parser = bibtex.Parser()
    bib_data = parser.parse_file(input_file)
    
    # Generate BBL content
    bbl_content = [
        r'\begin{thebibliography}{99}',
        ''
    ]
    
    # Sort entries by citation key
    sorted_entries = sorted(bib_data.entries.items())
    
    for key, entry in sorted_entries:
        bbl_content.append(format_bbl_entry(entry))
        bbl_content.append('')
    
    bbl_content.append(r'\end{thebibliography}')
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(bbl_content))
    
    click.echo(f'Successfully converted {input_file} to {output_file}')


if __name__ == '__main__':
    # Default configuration
    cfg_dict = {
        'input_file': 'bib_sample.bib',
        'output_file': 'bib_sample.bbl'
    }
    
    cfg = OmegaConf.create(cfg_dict) 
    cli_conf = OmegaConf.from_cli() 
    cfg = OmegaConf.merge(cfg, cli_conf) 

    print(f'converting {cfg.input_file} to {cfg.output_file}')
    convert(cfg.input_file, cfg.output_file)

    # In command line, run with:
    # python bib2bbl.py input_file=new.bib output_file=new.bbl

    
    
