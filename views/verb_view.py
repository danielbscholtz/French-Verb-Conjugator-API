from flask import Blueprint, request, jsonify
from database.__init__ import database
import json
from helpers.token_validation import validate_token
import requests
from bson.objectid import ObjectId
from controllers.verb_controller import create_favorite_verb, fetch_favorite_verb, fetch_all_favorite_verbs, delete_verb
import jwt
from app import app_config as config

verb = Blueprint("verb", __name__)

@verb.route("/v0/verb/", methods=["GET"])
def get_verb():
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication.'}), 401 
        
        data = json.loads(request.data)

        if 'verb' not in data:
            return jsonify({'error': 'Verb is needed in the request.'}), 400
        
        verb = data['verb']
        
        external_api_url = 'https://lasalle-frenchverb-api-afpnl.ondigitalocean.app/v1/api/verb'

        response = requests.get(external_api_url, headers={'token': '278ef2169b144e879aec4f48383dce28e654a009cacf46f8b6c03bbc9a4b9d11'}, json={'verb': verb})

        if response.status_code == 200:
            return jsonify({'verb': response.json()}), 200
        else:
            return jsonify({"error": response.json()["errorMessage"]})
    
    except Exception:
        return jsonify({'error': 'Something happened when getting verb.'}), 500

@verb.route("/v0/verb/random", methods=["GET"])
def get_random_verb():
    try:
            token = validate_token()

            if token == 400:
                return jsonify({'error': 'Token is missing in the request.'}), 400
            if token == 401:
                return jsonify({'error': 'Invalid token authentication.'}), 401
            
            data = json.loads(request.data)

            if 'quantity' not in data:
                return jsonify({'error': 'Quantity is needed in the request.'}), 400
            
            quantity = data['quantity'] 

            external_api_url = 'https://lasalle-frenchverb-api-afpnl.ondigitalocean.app/v1/api/verb/random'

            response = requests.get(external_api_url, headers={'token':'278ef2169b144e879aec4f48383dce28e654a009cacf46f8b6c03bbc9a4b9d11'}, json={'quantity': quantity})

            print(response.json())


            if response.status_code == 200:
                return jsonify({'quantity': response.json()}), 200
            else:
                return jsonify({"error": response.json()["errorMessage"]})
               
    except Exception as err:
        return jsonify({'error': 'Something happened when getting random verbs.', 'exception': str(err)}), 500

@verb.route("/v0/verb/favorite", methods=["POST"])
def favorite_verb():
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication.'}), 401 
            
        data = json.loads(request.data)

        if 'verb' not in data or data["verb"] == "":
            return jsonify({'error': 'Verb is needed in the request.'}), 400
        
        verb = data['verb']
        uid = token['uid']

        created_favoriteVerb = create_favorite_verb(uid, verb)

        if created_favoriteVerb == "Duplicated Verb":
            return "Duplicated Verb, please try another verb.", 401

        return jsonify({'status': 'Favorite verb created with success!', 'id': str(created_favoriteVerb.inserted_id)}), 200
        
    except Exception as err:
        print("Error in favorite_verb route: ", err), 500

@verb.route("/v0/verb/favorite/<favId>", methods=["GET"])
def get_favorite_verb(favId):
    try:

        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication.'}), 401 
        
        if not fetch_favorite_verb(favId):
            return "Verb isn't favorite"

        return fetch_favorite_verb(favId)

    except Exception as err:
        print("Error in favorite_verb route: ", err), 500

@verb.route("/v0/verb/favorite/all", methods=["GET"])
def get_all_favorite_verbs():

    token = validate_token()

    if token == 400:
        return jsonify({'error': 'Token is missing in the request.'}), 400
    if token == 401:
        return jsonify({'error': 'Invalid token authentication.'}), 401 
    
    uid = token['uid']

    return jsonify({'favorite verbs': fetch_all_favorite_verbs(uid)})

@verb.route("/v0/verb/favorite/delete/<favId>", methods=["DELETE"])
def delete_favorite_verb(favId):
    try:

        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication.'}), 401 
       
        return delete_verb(favId)

    except Exception as err:
        print("Error in delete_verb route: ", err), 500