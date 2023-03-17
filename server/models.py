from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    created_at = db.Column(db.DateTime, default_server=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    scientist = db.relationship("Scientist", back_populates=("missions"))
    planet = db.relationship("Planet", back_populates=("missions"))
    
    serialize_rules = ("-created_at", "-updated_at", "-scientist.missions", "-scientist.planet",
                       "-planet.missions", "-planet.scientist")
    
    @validates("scientist")
    def validate_scientist(self, key, scientist):
        scientist = [science for science in Scientist.query.all()]
        mission = Mission.query.all()
        if scientist in mission:
            raise ValueError("scientist can only join mission once")
        return scientist









class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    field_of_study = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, default_server=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    missions = db.relationship("Mission", back_populates="scientist")
    planets = association_proxy("missions", "planet")
    serialize_rules = ("-created_at", "-updated_at", "-missions", "-planets.created_at",
                       "-planets.updated_at", "-planets.scientists")


    @validates("name")
    def validate_name(self, key, name):
          scientist = [science for science in Scientist.query.all()]
          if name in scientist:
              raise ValueError("name must be unique")




class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    distance_from_earth = db.Column(db.String)
    nearests_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, default_server=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    missions = db.relationship("Mission", back_populates="planet")
    scientists = association_proxy("missions", "scientist")
    serialize_rules = ("-created_at", "-updated_at", "-missions", "-scientists.planets")






