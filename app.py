from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask import make_response
from flask import redirect
from flask.globals import session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

import os

basedir = os.path.abspath(os.path.dirname(__file__)) 


app = Flask(__name__)
#CsrfProtect(app)
app.config['SECRET_KEY'] = 'hard to guess string'
#activa bootstrap
Bootstrap(app)
#base de datos
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite') 

db = SQLAlchemy(app) 


    

#clase formulario
class NameForm(FlaskForm):       
    name = StringField('Cual es tu nombre?', validators=[Required()])       
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('¡Parece que has cambiado tu nombre! !')                   
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)       

#paginas de error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404       

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(debug=True)



