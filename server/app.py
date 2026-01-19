from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Plant

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Create tables and seed default plant if empty (needed for tests)
with app.app_context():
    db.create_all()

    if Plant.query.count() == 0:
        default_plant = Plant(
            name="Aloe",
            image="./images/aloe.jpg",
            price=11.50
        )
        db.session.add(default_plant)
        db.session.commit()


# ----------------- ROUTES -----------------

# GET /plants - index route
@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200


# GET /plants/<id> - show route
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant_by_id(id):
    plant = Plant.query.get(id)

    if not plant:
        return make_response({"error": "Plant not found"}, 404)

    return jsonify(plant.to_dict()), 200


# POST /plants - create route
@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()

    new_plant = Plant(
        name=data.get('name'),
        image=data.get('image'),
        price=data.get('price')
    )

    db.session.add(new_plant)
    db.session.commit()

    return jsonify(new_plant.to_dict()), 201


# ----------------- RUN APP -----------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)

