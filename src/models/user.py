import uuid
import random, string
from sklearn.model_selection import train_test_split
from flask import session
from src.common.database import Database
import src.models.recommenders as recommenders


class User(object):

    def __init__(self, User_id, Username, Password, _id=None):
        self._id=uuid.uuid4().hex if _id is None else _id
        self.User_id=User_id
        self.Username=Username
        self.Password=Password

    @classmethod
    def get_by_userid(cls, User_id):
        data=Database.find_one('User', {'User_id':User_id})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_username(cls, Username):
        data = Database.find_one('User', {'Username': Username})
        if data is not None:
            return cls(**data)

    def save_to_mongo(self):
        Database.insert(collection='User',
                        data=self.json())

    def json(self):
        return {
            '_id':self._id,
            'User_id':self.User_id,
            'Username':self.Username,
            'Password':self.Password
        }

    @staticmethod
    def login_valid(Username, Password):
        user=User.get_by_username(Username)
        if user is not None:
            return user.Password==Password
        return False

    @classmethod
    def register(cls,Username, Password):
        user=cls.get_by_username(Username)
        if user is None:
            letters = string.ascii_lowercase
            user_id = ''.join(random.choice(letters) for i in range(15))
            new_user=cls(user_id,Username, Password)
            new_user.save_to_mongo()
            session['Username']=Username
            return True
        else:
            return False

    @staticmethod
    def login(Username):
        session['Username']=Username

    @staticmethod
    def logout():
        session['Username']=None

    @staticmethod
    def get_id_by_username(username):
        return Database.find_one_id('User',
            {'Username':username},
            {'User_id':True, '_id':False}
        )

    @staticmethod
    def recom_songs_by_user(variable, User_id):
        train_data, test_data = train_test_split(variable, test_size=0.20, random_state=0)
        is_model = recommenders.item_similarity_recommender_py()
        is_model.create(train_data, 'User_id ', 'song')
        user_items = is_model.get_user_items(User_id)
        return user_items
