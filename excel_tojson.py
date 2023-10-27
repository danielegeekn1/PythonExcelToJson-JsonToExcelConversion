from flask import Flask, request, render_template, send_file
import pandas as pd
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'excel_file' not in request.files:
        return "Nessun file caricato"

    file = request.files['excel_file']
    if file.filename == '':
        return "Nessun file selezionato"

    if file and file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)

        # Converti il DataFrame in JSON
        json_data = df.to_json(orient='records')

        # Scrivi il JSON in un file temporaneo
        with open('temp.json', 'w') as json_file:
            json_file.write(json_data)

        # Restituisci il file JSON al cliente per il download
        return send_file('temp.json', as_attachment=True, download_name='output.json')

    return "Errore: il file deve essere in formato Excel (.xlsx)"
@app.route('/json_to_excel', methods=['POST'])
def json_to_excel():
    if 'json_file' not in request.files:
        return "Nessun file caricato"

    file = request.files['json_file']
    if file.filename == '':
        return "Nessun file selezionato"

    if file and file.filename.endswith('.json'):
        data = json.load(file)
        df = pd.DataFrame(data)

        # Converti il DataFrame in un file Excel temporaneo
        excel_filename = 'temp.xlsx'
        df.to_excel(excel_filename, index=False)

        # Restituisci il file Excel al cliente per il download
        return send_file(excel_filename, as_attachment=True, download_name='output.xlsx')

    return "Errore: il file deve essere in formato JSON (.json)"

if __name__ == '__main__':
    app.run(debug=True)