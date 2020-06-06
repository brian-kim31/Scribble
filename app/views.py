from flask import render_template
from app import app

# Views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Scribble'
    return render_template('index.html',  title = title)


@app.route('/scribble')
def scribble():

    '''
    View scribble page function that returns the scribble details page and its data
    '''
    
    return render_template('scribble.html')