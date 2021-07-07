from flask import Flask, render_template
from flask import make_response
from flask import redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
Bootstrap(app)

class NameForm(FlaskForm):       
    name = StringField('Cual es tu nombre?', validators=[Required()])       
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():                   
        name = form.name.data                   
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

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



