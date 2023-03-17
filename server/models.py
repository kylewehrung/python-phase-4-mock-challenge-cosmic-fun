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
    name = db.Column(db.String, nullable=False)
    scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    created_at = db.Column(db.DateTime, default_server=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    scientist = db.relationship("Scientist", back_populates=("missions"))
    planet = db.relationship("Planet", back_populates=("missions"))
    serialize_rules = ("-scientist.missions", ("-planet.missions",
                        "-scientist.scientists", "-planet.planets", "-created_at", "-updated_at"))

    @validates("scientist")
    def validate_scientist(self, key, scientist):
        science_mission = [scientist.id for scientist in Mission.query.all()]
        if scientist in science_mission:
            raise ValueError("Scientist can only go on a mission once")
        return scientist








class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    field_of_study = db.Column(db.String)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, default_server=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    missions = db.relationship("Mission", back_populates="scientist")
    planets = association_proxy("missions", "planet")
    serialize_rules = ("-missions", "-created_at", "-updated_at", "-planets.created_at",
                       "-planets.updated_at", "-planets.scientists")


    @validates("name")
    def validate_name(self, key, name):
      scientist_name = [science.name for science in Scientist.query.all()]
      if name in scientist_name:
          raise ValueError("Name must be unique")
      
    # @validates("field_of_study")
    # def validate_field_of_study(self, key, field_of_study):
    #   field_of_stud = [study.id for study in Scientist.query.all()]
    #   if not field_of_study in field_of_stud:
    #       raise ValueError("Must have a field of study")
     






class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, default_server=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    missions = db.relationship("Mission", back_populates=("planet"))
    scientists = association_proxy("missions", "scientist")
    serialize_rules = ("-missions", "-created_at", "-updated_at", 
                       "-scientists.planets")







