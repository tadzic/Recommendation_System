from sklearn.model_selection import train_test_split

from src.common.database import Database
import src.models.recommenders as Recommenders

class Song_data(object):
    def __init__(self, song_id, title, release, artist_name, year, _id):
        self._id=_id
        self.song_id=song_id
        self.title=title
        self.release=release
        self.artist_name=artist_name
        self.year=year

    @staticmethod
    def search_songs(songName):
        songs = Database.find(collection='Song_data', query={
            "$text": {"$search":songName}
        })
        search_song = []
        for song in songs:
            song_title = song['title']
            song_artist = song['artist_name']
            song_short = song_title + " - " + song_artist
            search_song.append(song_short)
        return search_song

    @classmethod
    def find_song(cls,songName, songAuthor):
        song=Database.find_one(collection='Song_data', query={
            "$and":[
                {"title": songName},
                {"artist_name": songAuthor}
            ]
        })
        return cls(**song)
    @staticmethod
    def find_similar_songs(variable, listening_song):
        train_data, test_data = train_test_split(variable, test_size=0.20, random_state=0)
        is_model = Recommenders.item_similarity_recommender_py()
        is_model.create(train_data, 'User_id ', 'song')
        similar_songs=is_model.get_similar_items([listening_song])
        return similar_songs
