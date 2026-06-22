from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    memories = db.relationship('Memory', backref='pet', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'memory': [m.text for m in self.memories]
        }

class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)

    def to_dict(self):
        return { 'id': self.id, 'memory': self.text }

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return jsonify({"message": "Bichinhos da Memória API", "status": "ok"})

@app.route('/pets', methods=['GET'])
def list_pets():
    pets = Pet.query.all()
    return jsonify([p.to_dict() for p in pets])

@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return jsonify(pet.to_dict())

@app.route('/pets', methods=['POST'])
def create_pet():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': 'name is required'}), 400
    pet = Pet(name=name)
    memories = data.get('memory') or []
    try:
        db.session.add(pet)
        db.session.flush()  # get pet.id
        for m in memories:
            mem = Memory(text=m, pet_id=pet.id)
            db.session.add(mem)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'db error'}), 500
    return jsonify(pet.to_dict()), 201

@app.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    return jsonify({'message': 'deleted'})

@app.route('/pets/<int:pet_id>/memories', methods=['GET'])
def list_memories(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return jsonify([m.to_dict() for m in pet.memories])

@app.route('/pets/<int:pet_id>/memories', methods=['POST'])
def add_memory(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    data = request.get_json() or {}
    text = data.get('memory')
    if not text:
        return jsonify({'error': 'memory is required'}), 400
    mem = Memory(text=text, pet_id=pet.id)
    db.session.add(mem)
    db.session.commit()
    return jsonify(mem.to_dict()), 201

@app.route('/pets/<int:pet_id>/memories/<int:mem_id>', methods=['PUT'])
def update_memory(pet_id, mem_id):
    pet = Pet.query.get_or_404(pet_id)
    mem = Memory.query.filter_by(id=mem_id, pet_id=pet.id).first_or_404()
    data = request.get_json() or {}
    text = data.get('memory')
    if not text:
        return jsonify({'error': 'memory is required'}), 400
    mem.text = text
    db.session.commit()
    return jsonify(mem.to_dict())

@app.route('/pets/<int:pet_id>/memories/<int:mem_id>', methods=['DELETE'])
def delete_memory(pet_id, mem_id):
    pet = Pet.query.get_or_404(pet_id)
    mem = Memory.query.filter_by(id=mem_id, pet_id=pet.id).first_or_404()
    db.session.delete(mem)
    db.session.commit()
    return jsonify({'message': 'deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
