from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask import make_response
from flask import redirect
from flask.globals import session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


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
migrate = Migrate(app, db) 
 



    

#clase formulario
class NameForm(FlaskForm):       
    name = StringField('Cual es tu nombre?', validators=[Required()])       
    submit = SubmitField('Enviar')

#pagina index
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()    
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:  
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))


#pagina user
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



#MODELOS DEFINICIONES ORM

class Role(db.Model):       
    __tablename__ = 'roles'       
    id = db.Column(db.Integer, primary_key=True)       
    name = db.Column(db.String(64), unique=True)    
    users = db.relationship('User', backref='role', lazy='dynamic')    #relacion de usuarios con roles
          
    def __repr__(self):       
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) # relacion de usuarios con roles
    
    def __repr__(self):
        return '<User %r>' % self.username



if __name__ == '__main__':
    app.run(debug=True)



