from flask import render_template, Response, request
from app import app
from azure import ServiceImport
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/ajax', methods = ["POST"])
def ajax():
    serviceName = request.form['request']
    azureService = ServiceImport()
    jsonGridData = azureService.getJsonGridData(serviceName)

    return Response(json.dumps(jsonGridData), mimetype='application/json')