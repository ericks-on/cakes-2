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

@chat_bp.route('/', methods=['GET'])
@swag_from('documentation/chat/get_chats.yml')
@jwt_required()
def get_chats():
    """This endpoint returns all chats"""
    user = storage.get_user(get_jwt_identity())
    if not user:
        return jsonify({'message': 'Unauthorised user'}), 401
    if user.user_type == 'admin':
        chats = storage.all(Chat)
    else:
        chats = user.send_chats + user.received_chats
    
    sorted_chats = sorted(chats, key=lambda x: x.created_at, reverse=True)
    if user.user_type == 'admin':
        return_chats = []
        for chat in sorted_chats:
            return_chat = chat.to_dict()
            if chat.sender.user_type == 'admin':
                return_chat["sender"] = 'admin'
                return_chat["recepient"] = chat.recepient.username
            elif chat.recepient.user_type == 'admin':
                return_chat["sender"] = chat.sender.username
                return_chat["recepient"] = 'admin'
            else:
                return_chat["sender"] = chat.sender.username
                return_chat["recepient"] = chat.recepient.username
            return_chats.append(return_chat)
        return jsonify({'chats': return_chats}), 200

    return jsonify({'chats': [chat.to_dict() for chat in sorted_chats]}), 200