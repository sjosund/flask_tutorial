from flask import render_template, flash, redirect
from app import app
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Lars'}
    posts = [
        {
            'author':{'nickname':'John'},
            'body':'Yoyoyo'
        },
        {
            'author':{'nickname':'Byone'},
            'body':'Ja de aer ju sa'
        }
    ]
    return render_template(
        "index.html",
        title='Home',
        user=user,
        posts=posts
    )

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template(
        'login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'] # How come this is accessable?
    )

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found')
        return redirect(url_for('index'))
    posts = [
        { 'author': user, 'body': 'Test post #1'},
        { 'author': user, 'body': 'Test post #2'}
    ]
    return render_template(
        'user.html',
        user=user,
        posts=posts
    )
