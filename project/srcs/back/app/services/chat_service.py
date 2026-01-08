from app.core.config import Config
from app.dal.repositories.chat_repository import ChatRepository
from app.dal.models.message import Message
from app.dal.models.conversation import Conversation

class ChatService :
    @classmethod
    def send_message(cls, sender: int, reciever : int, message: str) :
        print ("here start!", flush=True)
        chat_id = cls.create_conversation(sender, reciever)
        print ("here!", flush=True)
        id_message = ChatRepository.insert_message(Message(conversation_id=chat_id, sender_id=sender, content=message, is_read=False))
        return id_message

    @classmethod
    def create_conversation(cls, user1_id: int, user2_id : int) :
        chat_id = ChatRepository.find_conversation(user1_id, user2_id)
        if not chat_id :
            chat_id =  ChatRepository.create_conversation(Conversation(user1_id=user1_id, user2_id=user2_id))
            return chat_id
        return chat_id.id

    @classmethod
    def get_messages(cls, user_id: int, chat_id: int) :
        chat = ChatRepository.get_messages(chat_id,user_id)
        return chat

    # @classmethod
    # def get_messages(cls, user_id: int, chat_id: int, start: int = 0, number: int = 10) :
    #     row = ChatRepository.find_conversation_by_id(chat_id)
    #     if row.user1_id != user_id and row.user2_id != user_id :
    #         raise Exception("Not Today!")

    #     chat = ChatRepository.get_messages(chat_id, start, number)
    #     return chat
    @classmethod
    def get_chats(cls, user_id: str) :
        return ChatRepository.get_chats(user_id)

    # @classmethod
    # def get_chats(cls, user_id: str, start: int, number: int = 10) :
    #     return ChatRepository.get_chats(user_id, start, number)