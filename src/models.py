from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstName": self.firstName,
            "lastname": self.lastname
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "characters_id": self.characters_id,
            "planets_id": self.planets_id,
            "vehicles_id": self.vehicles_id,
            "user_id": self.user_id
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(50))
    url = db.Column(db.String(50))
    height = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    home_world = db.Column(db.String(250))
    films = db.Column(db.String(250))
    species = db.Column(db.String(250))
    vehicles = db.Column(db.String(250))
    starship = db.Column(db.String(250))
    created = db.Column(db.String(250))
    edited = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='characters', lazy=True)
    
    def __repr__(self):
        return '<Characters %r>' % self.id

    def serialize1(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "url": self.url,
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "url": self.url,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "home_world": self.home_world,
            "films": self.films,
            "species": self.species,
            "vehicles": self.vehicles,
            "starship": self.starship,
            "created": self.created,
            "edited": self.edited,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    edited = db.Column(db.String(250), nullable=False)
    films = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    residents = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    surface_water = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    favorites = db.relationship('Favorites', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "url": self.url,
            "climate": self.climate,
            "created": self.created,
            "diameter": self.diameter,
            "edited": self.edited,
            "films": self.films,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "residents": self.residents,
            "rotation_period": self.rotation_period,
            "surface_water": self.surface_water,
            "terrain": self.terrain,
            # do not serialize the password, its a security breach
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    cargo_capacity = db.Column(db.String(250), nullable=False)
    consumables = db.Column(db.String(250), nullable=False)
    cost_in_credits = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(250), nullable=False)
    crew = db.Column(db.String(250), nullable=False)
    edited = db.Column(db.String(250), nullable=False)
    length = db.Column(db.String(250), nullable=False)
    manofactured = db.Column(db.String(250), nullable=False)
    max_atmosphering_speed = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250), nullable=False)
    passengers = db.Column(db.String(250), nullable=False)
    pilots = db.Column(db.String(250), nullable=False)
    films = db.Column(db.String(250), nullable=False)
    vehicle_class = db.Column(db.String(250), nullable=False)
    favorites = db.relationship('Favorites', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "url": self.url,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "cost_in_credits": self.cost_in_credits,
            "created": self.created,
            "crew": self.crew,
            "edited": self.edited,
            "length": self.length,
            "manofactured": self.manofactured,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "model": self.model,
            "passengers": self.passengers,
            "pilots": self.pilots,
            "films": self.films,
            "vehicle_class": self.vehicle_class,
            # do not serialize the password, its a security breach
        }