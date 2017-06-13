from os import chdir
from os.path import dirname

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


#home page
@app.route('/')
def view_homepage():
    return render_template('home-page.html')

#stories library with fake data for testing purposes
@app.route('/stories-library')
def view_storieslibrary():
    names = ["Sense 3", "How To Get Away With Eating Nutella", "Big Bang Geography", "Nashville Town"]
    authors = ["Sarah Greilsamer", "Adam Roy", "Justin Li", "Jonathan Veitch"]
    dates = ["1923", "2458", "1983", "2017"]
    origins = ["Zimbabwe", "U.S.A.", "Germany", "Australia"]
    types = ["fable", "fable", "poem", "play"]
    themes = ["Love, War", "Friendship", "Racism", "Learning"]
    return render_template('stories-library.html', names=names, authors=authors, dates=dates, origins=origins, types=types, themes=themes)

#page with training videos
@app.route('/training-videos')
def view_trainingvideos():
    return render_template('training-videos.html')

#gallery of photos from previous shows
@app.route('/photo-gallery')
def view_photogallery():
    return render_template('photo-gallery.html')

#page of frequently asked questions
@app.route('/faqs')
def view_faqs():
    return render_template('faqs.html')

#FIXME
#Create classes for story, video and photo
#Probably going to have to create processing functions


###CODE NOT TO BE CHANGED###

@app.route('/css/<file>')
def view_css(file):
    return send_from_directory('css', file)

if __name__ == '__main__':
    chdir(dirname(__file__))
    app.run(debug=True)

