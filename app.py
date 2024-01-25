from flask import Flask, jsonify, request, render_template
import pyodbc
from datetime import datetime
import Business as bs

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_data():
    objbussines = bs.BussinesLayer()
    return objbussines.get_data()


@app.route('/getUserName', methods=['POST'])
def getUserName():
    data = request.get_json()
    objbussines = bs.BussinesLayer()
    return objbussines.getUserName(data)

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()
    objbussines = bs.BussinesLayer()
    return objbussines.add_data(data)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    objbussines = bs.BussinesLayer()
    return objbussines.register(data)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    objbussines = bs.BussinesLayer()
    return objbussines.login(data)


if __name__ == "__main__":
    app.run(host="192.168.1.6",port=8000)  #port http://127.0.0.1:8080 port=8080