import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

import locale
from datetime import datetime

def has_month(str):
    months = ['gennaio', 
              'febbraio', 
              'marzo', 
              'aprile', 
              'maggio', 
              'giugno', 
              'luglio', 
              'agosto', 
              'settembre', 
              'ottobre', 
              'novembre', 
              'dicembre']
    longest_string_with_a_date = '30 settembre 2025'
    if len(str)>len(longest_string_with_a_date):
        return False
    for m in months:
        if m in str.lower():
            return True
    return False

def get_last_line(input_string):
    # Split the string by newline characters
    lines = input_string.split('\n')
    # Return the last line
    return lines[-1] if lines else ''

def parse_italian_date(date_str):
    # Set the locale to Italian
    locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

    # Define the date format
    date_format = '%d %B %Y'

    # Parse the date string
    parsed_date = datetime.strptime(date_str, date_format)

    return parsed_date
    parsed_date = parse_italian_date(italian_date_str)

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
                last_line = get_last_line(annote)
                if has_month(last_line):
                    try:
                        print(last_line+'\t'+str(parse_italian_date(last_line)))
                    except:
                        print(last_line)
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