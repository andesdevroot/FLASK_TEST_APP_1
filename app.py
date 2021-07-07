from flask import Flask, render_template
from flask import make_response
from flask import redirect
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

# decorator 
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)       






if __name__ == '__main__':
    app.run(debug=True)



