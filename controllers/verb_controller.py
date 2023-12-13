from app import app_config as config
from database.__init__ import database
from models.fav_verb_model import FavoriteVerb
from flask import jsonify
from bson.objectid import ObjectId

def create_favorite_verb(uid, parameter_verb):
    try:

        new_fav_verb  = FavoriteVerb()
        new_fav_verb.owner = uid
        new_fav_verb.verb = parameter_verb

        collection = database.dataBase[config.CONST_VERBS_COLLECTION]

        if collection.find({'owner': new_fav_verb.owner, 'verb': new_fav_verb.verb}):
            return "Duplicated Verb"    

        created_fav_verb = collection.insert_one(new_fav_verb.__dict__)

        return created_fav_verb
    
    except Exception as err:
        print("Error on creating user: ", err)

def fetch_favorite_verb(favId):
    try:

        favId= ObjectId(favId) 

        collection = database.dataBase[config.CONST_VERBS_COLLECTION]

        favorite_verb = collection.find_one({'_id': favId})
        
        if favorite_verb:
            fav_verb = {}
            fav_verb["id"] = str(favorite_verb['_id'])
            fav_verb["owner"] = favorite_verb['owner']
            fav_verb["verb"] = favorite_verb['verb']

            return jsonify({'favorite': fav_verb})
        else:
            return jsonify({'error': 'Favorite verb not found.'})
        
    except Exception as err:
        print("Error on trying to fetch favorite verb. ", err)


def fetch_all_favorite_verbs(id):
    try:
        collection = database.dataBase[config.CONST_VERBS_COLLECTION]

        user_favorite_verbs = collection.find({'owner': id})

        verbs = []

        for verb in user_favorite_verbs:

            verbs.append(str(verb["verb"]))

        return verbs
    
    except Exception as err:
        print("Error on trying to fetch all favorite verbs. ", err)

def delete_verb(favId):
    try:
        favId= ObjectId(favId) 
        
        collection = database.dataBase[config.CONST_VERBS_COLLECTION]

        deleted_verb = collection.delete_one({'_id': favId})

        if deleted_verb.deleted_count == 0:
            return "Verb isn't in favorite list"

        return jsonify({'verbs_affected': deleted_verb.deleted_count})
    
    except Exception as err:
         print("Error on trying delete favorite verb. ", err)