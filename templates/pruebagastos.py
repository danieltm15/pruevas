from flask import Flask
import flask
from flask.globals import request
app = Flask(__name__)

# ruta 
@app.route('/almacenar gastos', methods = ['POST','GET'])
# Ahora cuando alguien entre a esa ruta
def crud_entrada_gasto():
    if request.method == 'POST':
        # Almacenar informacion
        request.data = request.form
    elif request.method == 'GET':
        print("Llego un get")



    return 'Gasto almacenado'

