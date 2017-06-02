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
    _service_name = request.form['request']
    _azure_service = RRS()
    _json_grid_data = _azure_service.get_json_grid_data(_service_name)

    return Response(json.dumps(_json_grid_data), mimetype='application/json')

@app.route('/update', methods = ["POST"])
def update():
    formData = request.form['request']