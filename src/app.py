"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Characters, Planets
import json
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# A partir de aquí los endpoints

@app.route('/user', methods=['GET'])
def handle_hello():
    allusers = User.query.all()
    print(allusers)
    results = list(map(lambda item: item.serialize(), allusers))
    print(results)
    return jsonify(results), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_info_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    print(user.serialize())
    
    return jsonify(user.serialize()), 200

@app.route('/favorites', methods=['GET'])
def handle_favorites():
    allfavorites = Favorites.query.all()
    print(allfavorites)
    results = list(map(lambda item: item.serialize(), allfavorites))
    print(results)
    return jsonify(results), 200

@app.route('/characters', methods=['GET'])
def handle_characters():
    allcharacters = Characters.query.all()
    print(allcharacters)
    results = list(map(lambda item: item.serialize1(), allcharacters))
    print(results)
    return jsonify(results), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_info_characters(character_id):
    character = Characters.query.filter_by(id=character_id).first()
    print(character.serialize())
    
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    allplanets = Planets.query.all()
    print(allplanets)
    results = list(map(lambda item: item.serialize(), allplanets))
    print(results)
    return jsonify(results), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_info_planets(planets_id):
    planets = Planets.query.filter_by(id=planets_id).first()
    print(planets.serialize())
    
    return jsonify(planets.serialize()), 200

@app.route('/user/<int:fav_id>/favorites', methods=['GET'])
def handle_user_favorites(fav_id):
    allusersfavs = Favorites.query.filter_by(user_id=fav_id).all()
    print(allusersfavs)
    results = list(map(lambda item: item.serialize(), allusersfavs))
    print(results)
    return jsonify(results), 200

@app.route('/user', methods=['POST'])
def add_new_user():

    request_body = json.loads(request.data)
    print(request_body)

    user = User.query.filter_by(email=request_body["email"]).first()
    
    # for i in results:
    #     # emails = results[i]["email"]
    #     print(i)

    # print(emails)

    if user is None:
        usuario = User(email=request_body["email"], password=request_body["password"], username=request_body["username"], firstName=request_body["firstName"], lastname=request_body["lastname"])
        # print(usuario)

        db.session.add(usuario)
        db.session.commit()

        # return jsonify(request_body.serialize()), 200
        return jsonify("ok"), 200
    
    return jsonify("ese email ya está registrado"), 200


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

    if email != user.email or password != user.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@app.route("/profile", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()

    user = User.query.filter_by(email=current_user).first()

    response_body = {
        "msg": "ok",
        "user": user.serialize()
    }

    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_new_fav_planet(user_id, planet_id):

    planets = Planets.query.filter_by(id=planet_id).first()
    users = User.query.filter_by(id=user_id).first()
    favorites = Favorites(user_id=users.id, planets_id=planets.id)

    db.session.add(favorites)
    db.session.commit()

    return jsonify(favorites.serialize()), 200

@app.route('/user/<int:user_id>/favorites/characters/<int:characters_id>', methods=['POST'])
def add_new_fav_character(user_id, characters_id):
    
    characters = Characters.query.filter_by(id=characters_id).first()
    users = User.query.filter_by(id=user_id).first()
    favorites = Favorites(user_id=users.id, characters_id=characters.id)

    db.session.add(favorites)
    db.session.commit()

    return jsonify(favorites.serialize()), 200

@app.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(user_id,planet_id):

    fav_planet = Favorites.query.filter_by(user_id=user_id).filter_by(planets_id=planet_id).first()
    print(fav_planet.serialize())

    db.session.delete(fav_planet.serialize()["planets_id"])
    db.session.commit()

    return jsonify("ok"), 200

@app.route('/favorites/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    allcharacters = Favorites.query.filter_by(characters_id=character_id).all()
    allcharacters.pop(character_id)
    print(allcharacters)
    return jsonify(allcharacters)



# Hasta aquí los endpoints

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
