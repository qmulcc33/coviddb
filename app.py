from flask import Flask, render_template, jsonify, make_response
import json

from requests import get


def get_data(region):
    
    area_name = ["england","scotland","northern ireland","wales"]
    if region not in area_name: raise ValueError('Unknown territory')
    
    endpoint = (
        'https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=nation;areaName='+region+'&structure={"date":"date","areaName":"areaName","newCasesByPublishDate":"newCasesByPublishDate","cumCasesByPublishDate":"cumCasesByPublishDate","newDeathsByDeathDate":"newDeathsByDeathDate"}')
    
    response = get(endpoint, timeout=10)
    
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: { response.text }')
        
    return response.json()

app = Flask(__name__)

@app.route("/")
def homepage():
		return """<html>
<body>
<h1>UK Covid API Service</h1>
<h3>Created by Chin Ching Fung, Akos Reitz, Maria-Georgiana Duta, Patricia Dominik and Joseph Brennan</h3>
<b>Group: 33</b>
</body>
</html>"""

@app.route("/<string:region>")
def get_region(region):
	return jsonify(get_data(str(region)))

@app.route("/<string:region>/latest")
def get_latest(region):
    regional_data = get_data(str(region))
    for latest in regional_data['data']:
        return latest

@app.route("/<string:region>/<string:date>", methods=['GET'])
def get_date(region, date):
        response = {date:'Not Found'}
        region_data = get_data(str(region))
        regional = region_data['data']
        for covid_data in regional:
            if covid_data['date'] == date:
                return covid_data

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)
