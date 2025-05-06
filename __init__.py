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
    # Récupère les données de commits depuis l'API GitHub
    response = requests.get('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    commits = response.json()
    
    # Traitement des données
    commit_counts = {}
    for commit in commits:
        date_str = commit['commit']['author']['date']
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        minute_key = f"{date.hour}:{date.minute:02d}"
        commit_counts[minute_key] = commit_counts.get(minute_key, 0) + 1
    
    # Formatage pour le graphique
    chart_data = [['Minute', 'Nombre de commits']]
    for minute, count in sorted(commit_counts.items()):
        chart_data.append([minute, count])
    
    return jsonify(chart_data)

if __name__ == "__main__":
  app.run(debug=True)
