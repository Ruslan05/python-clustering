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
    _serviceName = request.form['request']
    _azureService = ServiceImport()
    _jsonGridData = _azureService.getJsonGridData(_serviceName)

    return Response(json.dumps(_jsonGridData), mimetype='application/json')