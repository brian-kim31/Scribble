from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import CommentForm, UpdateProfile
from .. import db
from flask_login import login_required
from ..models import User


# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    message = "Welcome to Scribble"
    title = 'Scribble'
    click_bait = 'In life, you only have 60 seconds to impress someone. 1 minute can make or break you. How do we make sure that you use your 1 minute to actually say something meaningful?'
    return render_template('index.html',  title = title, message = message, click_bait = click_bait)


@main.route('/scribble')
def scribble():

    '''
    View scribble page function that returns the scribble details page and its data
    '''
    title = 'Scribble'

    return render_template('scribble.html', title = title)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)
    
