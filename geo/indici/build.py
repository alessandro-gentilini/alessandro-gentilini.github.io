import os

def int_to_roman(num):
    """
    Converte un numero intero in una cifra romana.
    """
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

def genera_indice_html(nomi_file_input, nome_file_output='indice_analitico.html'):
    """
    Legge una lista di file di testo, unisce e ordina i termini e i numeri di pagina,
    e genera un file HTML con un indice analitico consolidato.

    Args:
        nomi_file_input (list): Una lista di percorsi dei file di testo da leggere.
        nome_file_output (str): Il nome del file HTML da generare.
    """
    indice_raw = {}
    volume_map = {file_name: int_to_roman(i+1) for i, file_name in enumerate(nomi_file_input)}

    for nome_file_input in nomi_file_input:
        try:
            with open(nome_file_input, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Errore: il file '{nome_file_input}' non è stato trovato. Verrà ignorato.")
            continue

        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                # Suddivide la riga in due parti al primo ':'
                termine, numeri_str = line.split(':', 1)
                termine = termine.strip()
                # Rimuove spazi bianchi e converte i numeri in una lista di interi
                numeri = [int(n) for n in numeri_str.strip().split(',') if n.strip()]
                
                # Unisce i numeri di pagina se il termine esiste già, altrimenti lo aggiunge
                if termine in indice_raw:
                    indice_raw[termine].extend([(n, nome_file_input) for n in numeri])
                else:
                    indice_raw[termine] = [(n, nome_file_input) for n in numeri]
            except ValueError as e:
                print(f"Attenzione: Riga mal formattata in '{nome_file_input}' ignorata: '{line.strip()}' - Errore: {e}")
                continue

    # Ordina i termini alfabeticamente e i numeri di pagina in modo crescente e unico
    termini_ordinati = sorted(indice_raw.keys())
    for termine in termini_ordinati:
        indice_raw[termine] = sorted(list(set(indice_raw[termine])), key=lambda x: (x[1], x[0]))

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
        .volume-label {{
            font-weight: normal;
            font-style: italic;
            color: #6b7280; /* Tailwind gray-500 */
            margin-right: 0.5rem;
        }}
    </style>
</head>
<body class="p-8">
    <div class="max-w-3xl mx-auto bg-white rounded-xl shadow-lg p-8 md:p-12">
        <h1 class="text-4xl md:text-5xl font-bold text-center mb-6 text-gray-800">Indice Analitico</h1>
        <p class="text-center text-gray-600 mb-8">Elenco dei termini e delle relative pagine, ordinato alfabeticamente.</p>
        
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

        # Genera la stringa dei numeri di pagina raggruppandoli per volume
        pagine_per_volume = {}
        for page_number, volume_name in pages:
            volume_label = volume_map.get(volume_name, volume_name)
            if volume_label not in pagine_per_volume:
                pagine_per_volume[volume_label] = []
            pagine_per_volume[volume_label].append(str(page_number))

        pagine_str_list = []
        for vol_label, page_list in pagine_per_volume.items():
            if len(nomi_file_input) > 1:
                pagine_str_list.append(f"<span class='volume-label'>{vol_label}</span>{', '.join(page_list)}")
            else:
                pagine_str_list.append(f"{', '.join(page_list)}")
        
        pagine_str = ", ".join(pagine_str_list)

        # Aggiunge il termine e i numeri di pagina
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

# Chiamata alla funzione con una lista di nomi di file di input
if __name__ == '__main__':
    # Sostituisci i nomi dei file di esempio con i nomi dei tuoi file di testo
    # Per questo esempio, ho creato un input_vol1, input_vol2 ecc. che dovrai creare.
    file_di_testo = ['indice_v01.txt','indice_v02.txt']
    genera_indice_html(file_di_testo)