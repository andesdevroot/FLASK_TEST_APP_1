from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return 'Holaaaa, Cesarrr!'

@app.route('/saludo/<nombre>')
def saludo(nombre):
    return 'Hola, %s!' % nombre
    


if __name__ == '__main__':
    app.run(debug=True)



