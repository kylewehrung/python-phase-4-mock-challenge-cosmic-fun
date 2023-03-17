from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Scientist, Planet, Mission
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


class Scientists(Resource):

    def get(self):
        scientist = [sci.to_dict() for sci in Scientist.query.all()]
        return make_response(
            scientist, 
            200
        )
    

    def post(self):
        data = request.get_json()
        try:
            new_scientist = Scientist(
                name = data["name"],
                field_of_study = data["field_of_study"],
                avatar = data["avatar"]
            )
            db.session.add(new_scientist)
            db.session.commit()

        except Exception as e:
            message = {
                "errors": [e.__str__()]
            }
            return make_response(
                message, 
                422
            )
        
        return make_response(
            new_scientist.to_dict(),
            201
            )


api.add_resource(Scientists, "/scientists")






class ScientistsByID(Resource):
    
    def get(self, id):
        scientist = Scientist.query.filter_by(id=id).first().to_dict()
        if not scientist:
            return make_response({
                "errors": "scientist not found"
            }, 404)
        
        return make_response(
            scientist,
            200
        )


    def patch(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        if not scientist:
            return make_response({
                "errors": "scientist not found"
            }, 404)

        data = request.get_json()
        try:
            for attr in data:
                setattr(scientist, attr, data[attr])

            db.session.add(scientist)
            db.session.commit()

        except Exception as e:
            message = {
                "errors": [e.__str__()]
            }
            return make_response(
                message,
                422
            )
        
        return make_response(
            scientist.to_dict(), 
            201)
        


    def delete(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        if not scientist:
            return make_response({
                "errors": "scientist not found"
            }, 404)

        try:
            db.session.delete(scientist)
            db.session.commit()

        except Exception as e:
            message = {
                "errors": [e.__str__()]
            }
            return make_response(
                message,
                422
            )
        return make_response({
            "scientist deleted", 200
        })


api.add_resource(ScientistsByID, "/scientists/<int:id>")









class Planets(Resource):

    def get(self):
        planets = [planet.to_dict() for planet in Planet.query.all()]
        return make_response(
            planets,
            200
        )
    
api.add_resource(Planets, "/planets")









class Missions(Resource):

    def post(self):
        data = request.get_json()
        try:
            new_mission = Mission(
                name = data["name"],
                scientist_id = data["scientist_id"],
                planet_id = data["planet_id"]
            )

            db.session.add(new_mission)
            db.session.commit()


        except Exception as e:
            message = {
                "errors": [e.__str__()]
            }
            return make_response(
                message,
                422
            )
        
        return make_response(
            new_mission.to_dict(),
            201
        )


api.add_resource(Missions, "/missions")












if __name__ == '__main__':
    app.run(port=5555)
