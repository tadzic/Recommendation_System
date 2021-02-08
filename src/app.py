from flask import Flask, render_template, request, session

from src.common.database import Database
from src.models.song_data import Song_data
from src.models.user import User
from src.models.recomSystem import RecomSystem
from src.models.triplet_file import Triplet_file

app = Flask(__name__)
app.secret_key = "jose"

def first_load():
    initial = RecomSystem.Algorithm()
    return initial

variable=first_load()

@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login') #127.0.0.1.4990/login
def login_template():
    return render_template('login.html')


@app.route('/register')
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/auth/login/<string:User_id>', methods=['POST'])
@app.route('/auth/login', methods=['POST'])
def login_user(User_id=None):
    Username=request.form['Username']
    Password=request.form['Password']

    if User.login_valid(Username, Password):
        User.login(Username)
        user = User.get_by_userid(User_id)
        if User_id is None:
            user = User.get_by_username(session['Username'])
    else:
        session['Username']=None

    songs = user.recom_songs_by_user(variable, user.User_id)
    return render_template('user_songs.html', songs=songs, username=user.Username, user_id=user.User_id)

@app.route('/logout')
def log_out():
    User.logout()
    return render_template('log_out.html')

@app.route('/auth/register', methods=['POST'])
def register_user():
    Username = request.form['Username']
    Password = request.form['Password']
    User.register(Username, Password)

    return render_template('profile.html', Username=session['Username'])


@app.route('/songs/<string:User_id>')
@app.route('/songs')
def user_songs(User_id = None):
    if User_id is not None:
        user = User.get_by_userid(User_id)
    else:
        user = User.get_by_username(session['Username'])
    variabla=variable
    songs = user.recom_songs_by_user(variabla,user.User_id)
    return render_template('user_songs.html', songs=songs, username=user.Username)

@app.route('/trending')
def trending_songs():
    recoms=variable['song'].head(15)
    return render_template('trending.html', recoms=recoms)

@app.route('/search_song', methods=['POST'])
def search_song():
    search_song=request.form['Search']
    songs=Song_data.search_songs(search_song)
    return render_template('search_songs.html', songs=songs, search=search_song)

@app.route('/song_play/<string:song_play>')
def song_play(song_play):
    lista=song_play.split(" - ")
    songName=lista[0]
    songAuthor=lista[1]
    song=Song_data.find_song(songName, songAuthor)
    username=session['Username']
    user=User.get_by_username(username)
    triplet_file=Triplet_file(user.User_id, song.song_id, 1)
    triplet_file.update_count()
    variabla=variable
    similar_songs=Song_data.find_similar_songs(variabla, song_play)
    songs=similar_songs['song']
    return render_template('song.html', song=song, song_play=song_play, similar_songs=songs)

if __name__ == '__main__':
    app.run(port=4990, debug=True)