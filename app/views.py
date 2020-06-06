from flask import render_template
from app import app
from .forms import CommentForm


# Views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    message = "Welcome to Scribble"
    title = 'Scribble'
    click_bait = 'In life, you only have 60 seconds to impress someone. 1 minute can make or break you. How do we make sure that you use your 1 minute to actually say something meaningful?'
    return render_template('index.html',  title = title, message = message, click_bait = click_bait)


@app.route('/scribble')
def scribble():

    '''
    View scribble page function that returns the scribble details page and its data
    '''
    title = 'Scribble'

    return render_template('scribble.html', title = title)



