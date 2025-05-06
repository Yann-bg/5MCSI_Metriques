from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

                                                                                                                                       
app = Flask(__name__)             

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_kelvin = list_element.get('main', {}).get('temp')
        if temp_kelvin is not None:
            temp_celsius = round(temp_kelvin - 273.15, 2)
            results.append({'Jour': dt_value, 'temp': temp_celsius})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route('/commits/')
def show_commits_chart():
    return render_template('commits.html')

@app.route('/api/commits')
def get_commits_data():
    try:
        # Configuration des headers pour l'API GitHub
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # URL de l'API GitHub (avec votre repository si nécessaire)
        repo_url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
        
        # Requête à l'API GitHub
        response = requests.get(repo_url, headers=headers)
        
        # Vérification de la réponse
        if response.status_code != 200:
            error_msg = f"Erreur API GitHub: {response.status_code}"
            if response.status_code == 403:
                error_msg += " - Limite de taux dépassée, utilisation des données locales"
                return get_local_commits_data()
            return jsonify({"error": error_msg}), 500
        
        commits = response.json()
        
        # Traitement des données
        commit_counts = {}
        for commit in commits:
            try:
                date_str = commit['commit']['author']['date']
                date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                hour_minute = f"{date.hour:02d}:{date.minute:02d}"
                commit_counts[hour_minute] = commit_counts.get(hour_minute, 0) + 1
            except (KeyError, ValueError) as e:
                continue
        
        # Transformation en format pour le graphique
        chart_data = [['Heure/Minute', 'Nombre de commits']]
        for time_slot in sorted(commit_counts.keys()):
            chart_data.append([time_slot, commit_counts[time_slot]])
        
        # Sauvegarde locale pour développement
        save_local_copy(chart_data)
        
        return jsonify(chart_data)
    
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": str(e)}), 500

def get_local_commits_data():
    """Récupère les données depuis un fichier local en cas d'échec API"""
    try:
        with open('static/commits_backup.json', 'r') as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({"error": "Aucune donnée locale disponible"}), 500

def save_local_copy(data):
    """Sauvegarde les données dans un fichier local pour développement"""
    if not os.path.exists('static'):
        os.makedirs('static')
    with open('static/commits_backup.json', 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
  app.run(debug=True)
