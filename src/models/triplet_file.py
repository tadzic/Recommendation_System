import uuid

from src.common.database import Database

class Triplet_file(object):

    def __init__(self, User_id, song_id, listen_count, _id=None):
        self._id=uuid.uuid4().hex if _id is None else _id
        self.User_id=User_id
        self.song_id=song_id
        self.listen_count=listen_count

    def json(self):
        return {
            '_id':self._id,
            'User_id ':self.User_id,
            'song_id':self.song_id,
            ' listen_count':self.listen_count
        }

    def update_count(self):
        exists=Database.find_one('Triplet_set', {
            "$and":[
                {"User_id ": self.User_id},
                {"song_id": self.song_id}
            ]
        })
        if exists is None:
            Database.insert('Triplet_set', self.json())
        else:
            Database.update_one('Triplet_set',
                                {"song_id": self.song_id, "User_id ": self.User_id},
                                {"$inc": {" listen_count": 1}}
                                )
