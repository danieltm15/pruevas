from flask import Flask, request
app = Flask(__name__)
PORT=5000
DEBUG=False

@app.route('/')
def alguien_entro_a_la_ruta():
	return 'Funciona!!!!'

if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
