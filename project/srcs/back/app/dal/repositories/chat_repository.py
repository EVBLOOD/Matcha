from app.dal.base_repository import BaseRepository
from app.dal.models.message import Message
from app.dal.models.conversation import Conversation

class ChatRepository(BaseRepository):
    _table_name_conversations = "conversations"
    _columns_conversations = [
        "id", "user1_id", "user2_id"
    ]
    _columns_insertion_conversations = [
        "user1_id", "user2_id"
    ]

    _table_name_messages = "messages"
    _columns_messages = [
        "id", "conversation_id", "sender_id", "content", "is_read"
    ]
    _columns_insertion_messages = [
        "conversation_id", "sender_id", "content", "is_read"
    ]

    @classmethod
    def create_conversation(cls, profile_data: Conversation) :
        norm_data = {
            'user1_id' : profile_data.user_id,
            'user2_id' : profile_data.url,
        }
        conversation_id = cls.insert(table_name=cls._table_name_conversations, columns=cls._columns_insertion_conversations, data=norm_data)
        return conversation_id

    @classmethod
    def insert_message(cls, profile_data: Message) :
        norm_data = {
            'conversation_id' : profile_data.user_id,
            'sender_id' : profile_data.url,
            'content' : profile_data.is_profile_picture,
            'is_read' : profile_data.is_profile_picture
        }
        id = cls.insert(table_name=cls._table_name_messages, columns=cls._columns_insertion_messages, data=norm_data)
        return id


    @classmethod # TODO: this is worng but keep for now
    def mark_read(cls, profile_data: Message) :
        norm_data = {
            'conversation_id' : profile_data.user_id,
            'is_read' : profile_data.is_profile_picture
        }
        picture_id = cls.insert(table_name=cls._table_name_messages, columns=cls._columns_insertion_messages, data=norm_data)
        return picture_id
    
    @classmethod
    def find_conversation_by_id(cls, id: int) :
        return cls.find_by_something(id=id)

    @classmethod
    def find_conversation(cls, user1_id: int, user2_id: int) : # TODO: this is worng but keep for now
        return cls.find_by_something(id=user1_id)
    
    @classmethod
    def get_messages(cls, chat_id: int, start: int = 0, number: int = 10) :  # TODO: this is worng but keep for now
        return None
    @classmethod
    def get_chats(cls, user_id: int, start: int = 0, number: int = 10) :  # TODO: this is worng but keep for now
        return None