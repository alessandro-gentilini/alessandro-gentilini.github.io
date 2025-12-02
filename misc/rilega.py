import os
import subprocess
import sys
import natsort

if len(sys.argv) < 2:
    print("Usage: python rilega.py <nome_cartella_senza_punto_slash_davanti_senza_slash_finale>")
    sys.exit(1)

folder_path = sys.argv[1].rstrip('/')

# Get a sorted list of all PDF files in the folder
pdf_files = natsort.natsorted([f for f in os.listdir(folder_path) if f.endswith('.pdf')])

os.chdir(folder_path)


command = 'pdftk '
for f in pdf_files:
    print(f)
    command = command + f + ' '

output_pdf = '../book-'+folder_path+'.pdf'
command = command + ' cat output ' + output_pdf

try:
    subprocess.run(command, check=True, shell=True)
    print(f'Merged PDFs successfully into {output_pdf}')
except subprocess.CalledProcessError as e:
    print(f'Error merging PDFs: {e}')