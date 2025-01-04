import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

def create_latex_from_bib(bib_file_path, output_tex_path):
    with open(bib_file_path, 'r', encoding='utf-8') as bib_file:
        parser = BibTexParser()
        #parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bib_file, parser=parser)
    
    with open(output_tex_path, 'w', encoding='utf-8') as tex_file:
        tex_file.write(r'\documentclass{article}' + '\n')
        tex_file.write(r'\usepackage{cite}' + '\n')
        tex_file.write(r'\usepackage{fontspec}' + '\n')
        tex_file.write(r'\setmainfont{Noto Serif}' + '\n')

        tex_file.write(r'\usepackage[utf8]{inputenc}' + '\n')
        tex_file.write(r'\begin{document}' + '\n')

        for entry in bib_database.entries:
            annote = entry.get('annote', None)
            if "twitter-tweet" in annote:
                continue
            citation_key = entry.get('ID', None)
            if annote and citation_key:
                tex_file.write(f'{annote}\n')
                tex_file.write(f'\\cite{{{citation_key}}}\n\n')
                tex_file.write(r'\par\noindent\rule{\textwidth}{0.4pt}')
                tex_file.write('\n\n')
        
        tex_file.write(r'\bibliographystyle{plain}' + '\n')
        tex_file.write(r'\bibliography{' + bib_file_path.replace('.bib', '') + '}' + '\n')
        tex_file.write(r'\end{document}' + '\n')

if __name__ == "__main__":
    input_bib_file = 'le_mie_note.bib'
    output_tex_file = 'le_mie_note.tex'
    create_latex_from_bib(input_bib_file, output_tex_file)