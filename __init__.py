from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

                                                                                                                                       
app = Flask(__name__)            #yo   

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
def commits_graph():
    response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    minutes_count = {}

    for commit in json_content:
        date_str = commit.get('commit', {}).get('author', {}).get('date')
        if date_str:
            date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_object.strftime('%H:%M')  # exemple : 11:57
            minutes_count[minute] = minutes_count.get(minute, 0) + 1

    # On trie les résultats
    results = sorted([{'minute': k, 'count': v} for k, v in minutes_count.items()], key=lambda x: x['minute'])

    return render_template("commits.html", data=results)



if __name__ == "__main__":
  app.run(debug=True)
