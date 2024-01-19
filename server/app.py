from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at).all()
        response = make_response(jsonify([message.to_dict() for message in messages]))
    elif request.method == 'POST':
        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username'],
        )
        db.session.add(message)
        db.session.commit()
        response = make_response(
            jsonify(message.to_dict()), 201
        )
       
    return response



@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        newMessageData = request.get_json()
        for key in newMessageData:
            setattr(message, key, newMessageData[key])

        db.session.add(message)
        db.session.commit()
        response = make_response(
            jsonify(message.to_dict()))

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response = jsonify({'message': f'deleted message {id}'}) 
    return response
if __name__ == '__main__':
    app.run(port=4000)
