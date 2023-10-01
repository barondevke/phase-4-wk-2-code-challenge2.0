from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import CheckConstraint
db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'
    id = db.Column(db.Integer, primary_key=True,unique=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.Date,default=datetime.utcnow)
    updated_at = db.Column(db.Date,default=datetime.utcnow)

class Power(db.Model):
    __tablename__ = 'power'
    id = db.Column(db.Integer, primary_key=True,unique=True)
    name = db.Column(db.String)
    description = db.Column(db.String(20))
    created_at = db.Column(db.Date,default=datetime.utcnow)
    updated_at = db.Column(db.Date,default=datetime.utcnow)

   



class HeroPower(db.Model):
    __tablename__ = 'hero_power'
    id = db.Column(db.Integer, primary_key=True,unique=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.Date,default=datetime.utcnow)

    updated_at = db.Column(db.Date,default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint(strength.in_(['Strong', 'Weak', 'Average'])),
    )

    hero = db.relationship('Hero', backref=db.backref('hero_powers', lazy='dynamic'))
    power = db.relationship('Power', backref=db.backref('power_heroes', lazy='dynamic'))


