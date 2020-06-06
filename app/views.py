from flask import render_template
from app import app

# Views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    
    return render_template('index.html')


@app.route('/scribble/<int:scribble_id>')
def scribble(scribble_id):

    '''
    View scribble page function that returns the scribble details page and its data
    '''
    message = 'Scribble'
    return render_template('scribble.html',id = scribble_id, message = message)