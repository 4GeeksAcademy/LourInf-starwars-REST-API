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
from models import db, Users, Planets, Characters #from models import Users

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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

"""
Here we create our endpoints:
"""

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        response_body = {}
        results = {}
        users = db.session.execute(db.select(Users)).scalars()
        print(users)
        # Option 1: For-in: We create an empty variable, iterate through it, and use the append method. Easier.
        list_users = []
        for row in users:
            list_users.append(row.serialize())
        results['users'] = [row.serialize() for row in users]
        # Option 2: Comprehension List: We create users, iterate through users, and return a list with the serialization of each one.
        # results['users'] = [row.serialize() for row in users]
        response_body['message'] = 'Users List'
        response_body['results'] = 'results'
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        print(data)
        response_body = {}
        # here we write the logic to save the registry in our DB:
        user = Users(email = data.get('email'),
                    password = data.get('password'),
                    is_active = True)
        db.session.add(user)
        db.session.commit()
        response_body ['user'] = user
        return response_body, 200
    
@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):  
    if request.method == 'GET':
        response_body = {}
        results = {}
        # option 1:
        user = db.session.get(Users, user_id)
        if not user:
            response_body['message'] = 'User does not exist'
            return response_body, 404
        # There are other options, for example this Option 2, but this one returns in HTML, not JSON: 
            # Retorna el valor encontrado o retorna un error 404 con la `description` que definimos
            # user = db.one_or_404(db.select(Users).filter_by(id=user_id), 
                   # description=f"User not found , 404")
        results['user'] = user.serialize()     
        response_body['message'] = "User found"
        response_body['results'] = results
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        user = db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()
        if not user:
            response_body['message'] = 'User does not exist'
            return response_body, 404
        user.email = data.get('email')
        db.session.commit()
        results['user'] = user.serialize()     
        response_body['message'] = "User updated"
        response_body['results'] = results
        return response_body, 200
    if request.method == 'DELETE':
        data = request.json
        user = db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()
        if not user:
            response_body['message'] = 'User does not exist'
            return response_body, 404
        db.session.delete(user)
        db.session.commit()
        user.email = data.get('email')
        results['user'] = user.serialize()     
        response_body['message'] = "User removed"
        return response_body, 200
        
#PLANETS:
@app.route('/planets', methods=['GET', 'POST'])
def handle_planets():
    if request.method == 'GET':
        response_body = {}
        results = {}
        planets = db.session.execute(db.select(Planets)).scalars()
        print(planets)
        # Option 1: For-in: We create an empty variable, iterate through it, and use the append method. Easier.
        list_planets = []
        for row in planets:
            list_planets.append(row.serialize())
        results['planets'] = [row.serialize() for row in planets]
        # Option 2: Comprehension List: We create planets, iterate through each, and return a list with the serialization of each one.
        # results['planets'] = [row.serialize() for row in planets]
        response_body['message'] = 'Planets List'
        response_body['results'] = 'results'
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        print(data)
        response_body = {}
        # here we write the logic to save the registry in our DB:
        planet = Planets(
            name=data.get('name'),
            description=data.get('description'),
            diameter=data.get('diameter'),
            rotation_period=data.get('rotation_period'),
            orbital_period=data.get('orbital_period'),
            gravity=data.get('gravity'),
            population=data.get('population'),
            climate=data.get('climate'),
            terrain=data.get('terrain'),
            surface_water=data.get('surface_water'),
            url=data.get('url'))
        db.session.add(planet)
        db.session.commit()
        response_body ['planet'] = planet
        return response_body, 200
    
@app.route('/planets/<int:planet_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_planet(planet_id):  
    if request.method == 'GET':
        response_body = {}
        results = {}
        # option 1:
        planet = db.session.get(Planets, planet_id)
        if not planet:
            response_body['message'] = 'Planet does not exist'
            return response_body, 404
        # There are other options, for example this Option 2, but this one returns in HTML, not JSON: 
            # Retorna el valor encontrado o retorna un error 404 con la `description` que definimos
            # user = db.one_or_404(db.select(Planets).filter_by(id=planet_id), 
                   # description=f"Planet not found , 404")
        results['planet'] = planet.serialize()     
        response_body['message'] = "Planet found"
        response_body['results'] = results
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        planet = db.session.execute(db.select(Planets).where(Planets.id == planet_id)).scalar()
        if not planet:
            response_body['message'] = 'Planet does not exist'
            return response_body, 404
        planet.name = data.get('name')
        db.session.commit()
        results['planet'] = planet.serialize()     
        response_body['message'] = "Planet updated"
        response_body['results'] = results
        return response_body, 200
    if request.method == 'DELETE':
        data = request.json
        planet = db.session.execute(db.select(Planets).where(Planets.id == planet.id)).scalar()
        if not planet:
            response_body['message'] = 'Planet does not exist'
            return response_body, 404
        db.session.delete(planet)
        db.session.commit()
        planet.name = data.get('name')
        results['planet'] = planet.serialize()     
        response_body['message'] = "Planet removed"
        return response_body, 200

#CHARACTERS:
@app.route('/characters', methods=['GET', 'POST'])
def handle_characters():
    if request.method == 'GET':
        response_body = {}
        results = {}
        characters = db.session.execute(db.select(Characters)).scalars() 
        # Option 1: For-in loop
        list_characters = [row.serialize() for row in characters] 
        # Option 2: List comprehension
        # results['characters'] = [row.serialize() for row in characters]
        results['characters'] = list_characters
        response_body['message'] = 'Characters List'
        response_body['results'] = results
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        response_body = {}
        # here we write the logic to save the registry in our DB:
        character = Characters(
            name=data.get('name'),
            description=data.get('description'),
            height=data.get('height'),
            mass=data.get('mass'),
            hair_color=data.get('hair_color'),
            skin_color=data.get('skin_color'),
            eye_color=data.get('eye_color'),
            birth_year=data.get('birth_year'),
            gender=data.get('gender'),
            homeworld=data.get('homeworld'),
            url=data.get('url'))
        db.session.add(character)
        db.session.commit()
        response_body['character'] = character.serialize()
        response_body['message'] = 'Character created'
        return response_body, 200

@app.route('/characters/<int:character_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_character(character_id):  
    if request.method == 'GET':
        response_body = {}
        results = {}
        character = db.session.get(Characters, character_id)
        if not character:
            response_body['message'] = 'Character does not exist'
            return response_body, 404
        results['character'] = character.serialize()     
        response_body['message'] = "Character found"
        response_body['results'] = results
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        character = db.session.execute(db.select(Characters).where(Characters.id == character_id)).scalar()
        if not character:
            response_body['message'] = 'Character does not exist'
            return response_body, 404
        character.name = data.get('name')
        character.description = data.get('description')
        # Update other fields as needed
        db.session.commit()
        results['character'] = character.serialize()     
        response_body['message'] = "Character updated"
        response_body['results'] = results
        return response_body, 200
    if request.method == 'DELETE':
        character = db.session.execute(db.select(Characters).where(Characters.id == character_id)).scalar()
        if not character:
            response_body['message'] = 'Character does not exist'
            return response_body, 404
        db.session.delete(character)
        db.session.commit()
        response_body['message'] = "Character removed"
        return response_body, 200 


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
