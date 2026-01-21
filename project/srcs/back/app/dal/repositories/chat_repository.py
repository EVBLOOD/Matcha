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
            'user1_id' : profile_data.user1_id,
            'user2_id' : profile_data.user2_id,
        }
        conversation_id = cls.insert(table_name=cls._table_name_conversations, columns=cls._columns_insertion_conversations, data=norm_data)
        return conversation_id

    @classmethod
    def insert_message(cls, profile_data: Message) :
        norm_data = {
            'conversation_id' : profile_data.conversation_id,
            'sender_id' : profile_data.sender_id,
            'content' : profile_data.content,
            'is_read' : profile_data.is_read
        }
        id = cls.insert(table_name=cls._table_name_messages, columns=cls._columns_insertion_messages, data=norm_data)
        return id


    @classmethod # TODO: this is worng but keep for now
    def mark_read(cls, profile_data: Message) :
        norm_data = {
            'conversation_id' : profile_data.conversation_id,
            'is_read' : profile_data.is_read
        }
        picture_id = cls.insert(table_name=cls._table_name_messages, columns=cls._columns_insertion_messages, data=norm_data)
        return picture_id
    
    @classmethod
    def find_conversation_by_id(cls, id: int) :
        return cls.find_by_something(id=id)

    @classmethod
    def find_conversation(cls, user1_id: int, user2_id: int) :
        query = "SELECT * FROM conversations WHERE (user1_id = %s AND user2_id = %s) OR (user1_id = %s AND user2_id = %s)"
        row = cls._fetch_one(query, (user1_id,user2_id, user2_id,user1_id))
        return Conversation(id=row[0], *(row[1:])) if row else None
    
    @classmethod
    def get_messages_page(cls, chat_id: int, user_id: int, limit: int = 50, before_id: int = None):        
        query = """
            SELECT 
                m.id, m.conversation_id, m.sender_id, m.content, 
                m.sent_at, m.is_read
            FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE m.conversation_id = %s
            AND (c.user1_id = %s OR c.user2_id = %s)
        """
        
        params = [chat_id, user_id, user_id]
        
        if before_id:
            query += " AND m.id < %s"
            params.append(before_id)
        
        query += " ORDER BY m.sent_at DESC LIMIT %s"
        params.append(limit)
        
        return cls._fetch_all(query, params)
    
    @classmethod
    def get_messages(cls, chat_id: int, user_id: int) :
        query = """
            SELECT
                c.id AS conversation_id,
                c.created_at,
                u.id AS peer_id,
                u.username,
                u.first_name,
                u.last_name,
                u.last_online,
                (SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture))
                    FROM user_pictures up
                    WHERE up.user_id = u.id AND up.is_profile_picture = TRUE)
                    AS profile_picture_url,
                (SELECT json_agg(json_build_object('id', ms.id, 'sender_id', ms.sender_id, 'sent_at',ms.sent_at, 'is_read' ,ms.is_read, 'content', ms.content))
                    FROM messages  ms
                    WHERE ms.conversation_id = c.id) AS messages_list
            FROM conversations AS c
            JOIN users u ON u.id = (
                CASE 
                    WHEN c.user1_id = %s THEN c.user2_id 
                    ELSE c.user1_id 
                END
            )
            WHERE (c.user1_id = %s OR c.user2_id = %s) AND c.id = %s;
            """
        params = (user_id, user_id,user_id, chat_id)
        return cls._fetch_all(query, params)
    
    @classmethod
    def get_chats(cls, user_id: int) :  # TODO: this is worng but keep for now
        query = """
            SELECT
                c.id AS conversation_id,
                COALESCE(
                    (SELECT MAX(m.sent_at) FROM messages m WHERE m.conversation_id = c.id),
                    c.created_at
                ) AS last_active_at,
                c.created_at,
                u.id AS peer_id,
                u.username,
                u.first_name,
                u.last_name,
                u.last_online,
                (SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture))
                    FROM user_pictures up
                    WHERE up.user_id = u.id AND up.is_profile_picture = TRUE)
                    AS profile_picture_url
            FROM conversations AS c
            JOIN users u ON u.id = (
                CASE 
                    WHEN c.user1_id = %s THEN c.user2_id 
                    ELSE c.user1_id 
                END
            )
            WHERE c.user1_id = %s OR c.user2_id = %s
            ORDER BY last_active_at DESC
            """
        params = (user_id, user_id,user_id)
        return cls._fetch_all(query, params)
    
    @classmethod
    def get_chats_page(cls, user_id: int, limit: int = 50, before_id: int = None):    
        query = """
            SELECT
                c.id AS conversation_id,
                c.created_at,
                u.id AS peer_id,
                u.username,
                u.first_name,
                u.last_name,
                u.last_online,
                (SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture))
                    FROM user_pictures up
                    WHERE up.user_id = u.id AND up.is_profile_picture = TRUE)
                    AS profile_picture_url
            FROM conversations AS c
            JOIN users u ON u.id = (
                CASE 
                    WHEN c.user1_id = %s THEN c.user2_id 
                    ELSE c.user1_id 
                END
            )
            WHERE c.user1_id = %s OR c.user2_id = %s;
            """
        params = (user_id, user_id,user_id)
        
        if before_id:
            query += " AND m.id < %s"
            params.append(before_id)
        
        query += " ORDER BY m.sent_at DESC LIMIT %s"
        params.append(limit)
        return cls._fetch_all(query, params)