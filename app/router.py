from flask import render_template, Response, request
from app import app
from azure import RRS
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/edit')
def edit():
    return render_template("edit.html")

@app.route('/getGridData', methods = ["POST"])
def getGridData():
    _serviceName = request.form['request']
    _azureService = RRS()
    _jsonGridData = _azureService.getJsonGridData(_serviceName)

    return Response(json.dumps(_jsonGridData), mimetype='application/json')

@app.route('/update', methods = ["POST"])
def update():
    formData = request.form['request']