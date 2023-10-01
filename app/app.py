#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Hero,HeroPower,Power

hero1 = Hero(name = "Kamala Khan", super_name= "Ms. Marvel")
hero2 = Hero(name= "Doreen Green", super_name= "Squirrel Girl" )
power1 = Power(name='Power',description='Power')
power2 = Power(name='Power2',description='Power2')
heroPower1 = HeroPower(hero_id=1,power_id=1,strength='Average')
heropower2=HeroPower(hero_id=1,power_id=2,strength='Average')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
CORS(app)

db.init_app(app)



@app.route('/')
def home():
    return ''

@app.route('/heroes')
def get_heroes():
    heroes = Hero.query.all()
    heroes_list = []
    for hero in heroes:
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        }
        heroes_list.append(hero_data)

    return (heroes_list, 200)

@app.route('/heroes/<int:id>')
def get_hero_by_id(id):
    hero = Hero.query.filter(Hero.id == id).first()
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404

    hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            
        }
    HeroPowers = HeroPower.query.filter(HeroPower.hero_id == id).all()
    power_list = []

    for heroPower in HeroPowers:
            power = Power.query.filter(Power.id == heroPower.power_id).first()
            if power:
                power_data = {
                    "id": power.id,
                    "name": power.name,
                    "description": power.description
                }
                power_list.append(power_data)
    hero_data['powers'] = power_list

    
    return jsonify(hero_data)
    
@app.route('/powers')
def get_power():
    powers = Power.query.all()
    power_list = []
    for power in powers:
        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        power_list.append(power_data)

    return (power_list, 200)

@app.route('/powers/<int:id>')
def get_power_by_id(id):
    power = Power.query.filter(Power.id == id).first()
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }

    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['PUT'])
def edit_power(id):
    power = Power.query.filter(Power.id == id).first()
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    
    power.description = request.json['description']
    db.session.commit()
    power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
    return jsonify(power_data)

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    heroPower = HeroPower(hero_id=request.json['hero_id'],power_id=request.json['power_id'],strength=request.json['strength'])
    db.session.add(heroPower)
    db.session.commit()
    return get_hero_by_id(request.json['hero_id'])



if __name__ == '__main__':
    app.run(port=5555)
