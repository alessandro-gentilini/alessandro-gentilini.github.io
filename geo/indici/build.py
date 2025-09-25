import os

def genera_indice_html(nome_file_input, nome_file_output='indice_analitico.html'):
    """
    Legge un file di testo, ordina i termini e i numeri di pagina,
    e genera un file HTML con un indice analitico.

    Args:
        nome_file_input (str): Il percorso del file di testo da leggere.
        nome_file_output (str): Il nome del file HTML da generare.
    """
    try:
        with open(nome_file_input, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Errore: il file '{nome_file_input}' non è stato trovato.")
        return

    indice_raw = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            # Suddivide la riga in due parti al primo ':'
            termine, numeri_str = line.split(':', 1)
            # Rimuove spazi bianchi e converte i numeri in una lista di interi
            numeri = [int(n) for n in numeri_str.strip().split(',') if n.strip()]
            indice_raw[termine.strip()] = sorted(numeri)
        except ValueError as e:
            print(f"Attenzione: Riga mal formattata ignorata: '{line.strip()}' - Errore: {e}")
            continue

    # Ordina i termini alfabeticamente
    termini_ordinati = sorted(indice_raw.keys())

    # Genera il contenuto HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indice Analitico</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap');
        body {{
            font-family: 'Merriweather', Georgia, serif;
            background-color: #f3f4f6;
            color: #333;
        }}
        .drop-cap-container {{
            display: flex;
            align-items: center;
        }}
        .drop-cap {{
            font-size: 3.5em;
            font-weight: bold;
            line-height: 1;
            color: #1e40af; /* Tailwind blue-800 */
            margin-right: 0.25em;
            padding-top: 0.1em;
        }}
        .index-list {{
            list-style: none;
            padding-left: 0;
        }}
        .index-item {{
            margin-bottom: 0.5rem;
            line-height: 1.5;
        }}
        .page-numbers {{
            font-weight: bold;
            color: #555;
            float: right;
        }}
        .divider {{
            border-bottom: 1px solid #e5e7eb;
            margin: 1.5rem 0;
        }}
    </style>
</head>
<body class="p-8">
    <div class="max-w-3xl mx-auto bg-white rounded-xl shadow-lg p-8 md:p-12">
        <h1 class="text-4xl md:text-5xl font-bold text-center mb-6 text-gray-800">Indice analitico dei quaderni neri</h1>
        <div class="index-container">
    """

    last_initial = None
    for termine in termini_ordinati:
        pages = indice_raw[termine]
        current_initial = termine[0].upper()
        
        # Aggiunge un capilettera per ogni nuova lettera iniziale
        if current_initial != last_initial:
            if last_initial is not None:
                html_content += """
                <div class="divider"></div>
                """
            html_content += f"""
            <div class="flex items-center mb-4 mt-8">
                <span class="drop-cap">{current_initial}</span>
            </div>
            """
            last_initial = current_initial

        # Aggiunge il termine e i numeri di pagina
        pagine_str = ", ".join(map(str, pages))
        html_content += f"""
            <div class="flex justify-between items-start index-item">
                <span class="text-lg font-medium">{termine}</span>
                <span class="text-sm md:text-base page-numbers">{pagine_str}</span>
            </div>
        """

    html_content += """
        </div>
    </div>
</body>
</html>
    """

    with open(nome_file_output, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"File HTML '{nome_file_output}' generato con successo.")

# Chiamata alla funzione con il nome del file di input
if __name__ == '__main__':
    genera_indice_html('indice_v01.txt')