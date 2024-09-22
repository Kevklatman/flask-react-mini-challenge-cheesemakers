from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import Cheese, Producer, db

# from flask_restful import Api, Resource




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# api = Api(app)



@app.route("/")
def index():
    response = make_response({"message": "Hello Fromagers!"}, 200)
    return response
#producer get routes

@app.route("/producers")
def producers():
    producers = Producer.query.all()
    producers_list = [producer.to_dict() for producer in producers]

    response = make_response(
        jsonify(producers_list),
        200
    )
    return response

@app.route('/producers/<int:id>', methods=['GET', 'DELETE'])
def producer_by_id(id):
    producer = Producer.query.filter(Producer.id == id).first()

    if not producer:
        return make_response(jsonify({"error": "Resource not found"}), 404)

    if request.method == 'GET':
        producer_dict = producer.to_dict_with_cheeses()
        response = make_response(
            jsonify(producer_dict),
            200
        )
        return response

    elif request.method == 'DELETE':
        try:
            Cheese.query.filter_by(producer_id=id).delete()
            
            db.session.delete(producer)
            db.session.commit()

            return '', 204

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)
#post cheeses       
@app.route('/cheeses', methods=['POST'])
def create_cheese():
    data = request.json

    if not all(key in data for key in ['kind', 'is_raw_milk', 'production_date', 'image', 'price', 'producer_id']):
        return make_response(jsonify({"errors": ["validation errors"]}), 400)

    producer = Producer.query.get(data['producer_id'])
    if not producer:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)

    try:
        new_cheese = Cheese(
            kind=data['kind'],
            is_raw_milk=data['is_raw_milk'],
            production_date=datetime.strptime(data['production_date'], "%Y-%m-%d"),
            image=data['image'],
            price=float(data['price']),
            producer_id=data['producer_id']
        )

        db.session.add(new_cheese)
        db.session.commit()

        response_data = {
            "id": new_cheese.id,
            "image": new_cheese.image,
            "is_raw_milk": new_cheese.is_raw_milk,
            "kind": new_cheese.kind,
            "price": new_cheese.price,
            "producer": {
                "name": producer.name
            },
            "producer_id": new_cheese.producer_id,
            "production_date": new_cheese.production_date.strftime("%Y-%m-%d %H:%M:%S")
        }

        return make_response(jsonify(response_data), 201)

    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"errors": ["validation errors"]}), 400)
    

@app.route('/cheeses/<int:id>', methods=['PATCH'])
def update_cheese(id):
    cheese = Cheese.query.get(id)
    if not cheese:
        return make_response(jsonify({"errors": ["Cheese not found"]}), 404)

    data = request.json

    try:
        if 'is_raw_milk' in data:
            cheese.is_raw_milk = data['is_raw_milk']
        if 'production_date' in data:
            cheese.production_date = datetime.strptime(data['production_date'], "%Y-%m-%d")
        if 'kind' in data:
            cheese.kind = data['kind']
        if 'image' in data:
            cheese.image = data['image']
        if 'price' in data:
            cheese.price = float(data['price'])
        if 'producer_id' in data:
            cheese.producer_id = data['producer_id']

        db.session.commit()

        response_data = {
            "id": cheese.id,
            "image": cheese.image,
            "is_raw_milk": cheese.is_raw_milk,
            "kind": cheese.kind,
            "price": cheese.price,
            "producer_id": cheese.producer_id,
            "production_date": cheese.production_date.strftime("%Y-%m-%d %H:%M:%S")
        }

        return make_response(jsonify(response_data), 200)

    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"errors": ["validation errors"]}), 400)


if __name__ == "__main__":
    app.run(port=5555, debug=True)

#Routes 
#1. GET/ producers
#2. 
