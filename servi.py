from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def alguien_entro_a_la_ruta():
	return 'Funciona!!!!'

if __name__ == "__main__":
    app.run()
