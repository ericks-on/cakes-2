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

@chat_bp.route('/<chat_id>', methods=['GET'])
@swag_from('documentation/chat/get_chat.yml')
@jwt_required()
def get_chat(chat_id):
    """This endpoint returns a specific chat"""
    user = storage.get_user(get_jwt_identity())
    if not user:
        return jsonify({'message': 'Unauthorised user'}), 401
    chat = storage.get(Chat, chat_id)

    if not chat:
        return jsonify({'message': 'Chat not found'}), 404
    if user.user_type == 'admin':
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
        return jsonify({'chat': return_chat}), 200
    if user.id not in [chat.sender_id, chat.recepient_id]:
        return jsonify({'message': 'Unauthorised user'}), 401
    return jsonify({'chat': chat.to_dict()}), 200

@chat_bp.route('/<chat_id>', methods=['DELETE'])
@swag_from('documentation/chat/delete_chat.yml')
@jwt_required()
def delete_chat(chat_id):
    """This endpoint deletes a specific chat"""
    user = storage.get_user(get_jwt_identity())
    if not user:
        return jsonify({'message': 'Unauthorised user'}), 401
    chat = storage.get(Chat, chat_id)
    if not chat:
        return jsonify({'message': 'Chat not found'}), 404
    if user.user_type == 'admin':
        storage.delete(chat)
        storage.save()
        return jsonify({'message': 'Chat deleted'}), 200
    if user.id not in [chat.sender_id, chat.recepient_id]:
        return jsonify({'message': 'Unauthorised user'}), 401
    storage.delete(chat)
    storage.save()
    return jsonify({'message': 'Chat deleted'}), 200

@chat_bp.route('/<chat_id>/messages', methods=['POST'])
@swag_from('documentation/chat/create_message.yml')
@jwt_required()
def create_message(chat_id):
    """This endpoint creates a new message"""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    user = storage.get_user(get_jwt_identity())
    chat = storage.get(Chat, chat_id)
    if not user:
        return jsonify({'message': 'Unauthorised user'}), 401
    if not chat:
        return jsonify({'message': 'Chat not found'}), 404
    if user.user_type != 'admin':
        if user.id not in [chat.sender_id, chat.recepient_id]:
            return jsonify({'message': 'Unauthorised user'}), 401
        # if user.id == chat.sender_id:
        #     if chat.sender_deleted == 1:
        #         return jsonify({'message': 'Chat not found'}), 404
        # else:
        #     if chat.recepient_deleted == 1:
        #         return jsonify({'message': 'Chat not found'}), 404
    content = data.get('content')
    if not content:
        return jsonify({'message': 'No content provided'}), 400
    new_message = Message(chat_id=chat.id, content=content, sender_id=user.id)
    storage.add(new_message)
    storage.save()
    obj = storage.get(Message, new_message.id)
    return jsonify({'message': obj.to_dict()}), 201

@chat_bp.route('/<chat_id>/messages', methods=['GET'])
@swag_from('documentation/chat/get_messages.yml')
@jwt_required()
def get_messages(chat_id):
    """This endpoint returns all messages in a chat"""
    user = storage.get_user(get_jwt_identity())
    if not user:
        return jsonify({'message': 'Unauthorised user'}), 401
    chat = storage.get(Chat, chat_id)
    if not chat:
        return jsonify({'message': 'Chat not found'}), 404
    if user.user_type != 'admin':
        if user.id not in [chat.sender_id, chat.recepient_id]:
            return jsonify({'message': 'Unauthorised user'}), 401
        # if user.id == chat.sender_id:
        #     if chat.sender_deleted == 1:
        #         return jsonify({'message': 'Chat not found'}), 404
        # else:
        #     if chat.recepient_deleted == 1:
        #         return jsonify({'message': 'Chat not found'}), 404
    messages = chat.messages
    sorted_messages = sorted(messages, key=lambda x: x.created_at, reverse=True)
    return jsonify({'messages': [message.to_dict() for message in sorted_messages]}), 200