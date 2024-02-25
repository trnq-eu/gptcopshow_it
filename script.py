import os
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader
import yaml
import datetime

# Ottieni la directory di lavoro corrente
current_working_directory = os.getcwd()

template_env = Environment(loader=FileSystemLoader(searchpath='./site/templates'))

index_template = template_env.get_template('index_layout.html')
case_template = template_env.get_template('case_layout.html')

md_pages_dir = os.path.join(current_working_directory, 'site/md_pages')

md_files = [file for file in os.listdir(md_pages_dir) if file.endswith('.md')]

cases = []

for md_file in md_files:
    # Ricostruisce i file di tutte le pagine in markdown
    md_path = os.path.join(md_pages_dir, md_file)

    # Stampa il percorso del file Markdown
    print(f'Processing {md_path}')

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

        # Estrai i metadati dal blocco YAML
        _, yaml_block, markdown_content = content.split('---', 2)
        metadata = yaml.safe_load(yaml_block)

        # Converti la data in un oggetto datetime.date
        date_obj = metadata.get('date', None)
        if date_obj and not isinstance(date_obj, datetime.date):
            date_obj = datetime.datetime.strptime(date_obj, '%Y-%m-%d').date()

        # Genera le pagine html dei singoli casi
        output_file = f"{os.path.splitext(md_file)[0]}_output.html"
        output = case_template.render(
            date=date_obj,
            title=metadata.get('title', 'senza titolo'),
            case_number=metadata.get('case_number', 'senza numero'),
            content=markdown(markdown_content)
        )

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'Genera {output_file} from {md_file}')

        cases.append({
            'date': date_obj,
            'title': metadata.get('title', 'senza titolo'),
            'case_number': metadata.get('case_number', 'senza numero'),
            'filename': output_file
        })

# Ordina gli articoli per data dal più recente
sorted_cases = sorted(cases, key=lambda x: x['case_number'], reverse=True)

# Inserisci i dati all'interno del template
index_output = index_template.render(cases=sorted_cases)

# Salva il risultato nella home page
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_output)

print('Home page aggiornata')
print(current_working_directory)

# Stampa a console il contenuto della lista dei casi
print("Elenco dei casi:")
for case in cases:
    print(case)