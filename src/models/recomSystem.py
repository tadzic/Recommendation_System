import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from src.models import recommenders
from src.common.database import Database
from src.models.song_data import Song_data


class RecomSystem(object):

    Database.initialize()

    @staticmethod
    def Algorithm():
        triplet_file = Database.find('Triplet_set', {"song_id": {"$exists": True}})
        triplet = list(triplet_file)
        triplet_filePandas = pd.DataFrame(triplet)
        song_data = Database.find('Song_data', {"song_id": {"$exists": True}})
        song = list(song_data)
        song_dataPandas = pd.DataFrame(song)
        song_df = pd.merge(triplet_filePandas, song_dataPandas.drop_duplicates(['song_id']), on="song_id", how="left")
        song_df['song'] = song_df['title'].map(str) + " - " + song_df['artist_name']
        song_grouped = song_df.groupby(['song']).agg({' listen_count': 'count'}).reset_index()
        grouped_sum = song_grouped[' listen_count'].sum()
        song_grouped['percentage'] = song_grouped[' listen_count'].div(grouped_sum) * 100
        song_grouped.sort_values([' listen_count', 'song'], ascending=[0, 1])
        return song_df
