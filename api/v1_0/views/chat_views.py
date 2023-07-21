from flask import Blueprint, request, jsonify, make_response
from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.chat import Chat
from models.message import Message
from models import storage


chat_bp = Blueprint('chat_bp', __name__, url_prefix='/chats')


@chat_bp.route('/', methods=['POST'])
@swag_from('documentation/chat/create_chat.yml')
@jwt_required()
def create_chat():
    """This endpoint creates a new chat"""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    sender =  storage.get_user(get_jwt_identity())
    recepient = storage.get_user(data.get('recepient'))
    subject = data.get('subject')

    if not sender:
        return jsonify({'message': 'Unauthorised user'}), 401
    if not recepient:
        return jsonify({'message': 'No recepient_id provided'}), 400
    if not subject:
        return jsonify({'message': 'No subject provided'}), 400
    if sender == recepient:
        return jsonify({'message': 'You cannot send yourself a message'}), 403

    new_chat = Chat(sender_id=sender.id, recepient_id=recepient.id,
                    subject=subject)
    storage.add(new_chat)
    storage.save()
    obj = storage.get(Chat, new_chat.id)
    return jsonify({'chat': obj.to_dict()}), 201

