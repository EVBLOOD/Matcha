from app.dal.base_repository import BaseRepository
from app.dal.models.user_interests import UserInterests

class UserInterestsRepository(BaseRepository):
    _table_name = "user_interests"
    _columns = [
        "user_id", "tag_id"
    ]

    @classmethod
    def create_user_interests(cls, user_interest: UserInterests, injected_cursor = None) :
        norm_data = {
            'user_id' : user_interest.user_id,
            'tag_id' : user_interest.tag_id,
        }
        tag_id = cls.insert(table_name=cls._table_name, columns=cls._columns, data=norm_data, returning="tag_id", injected_cursor=injected_cursor)
        return tag_id

    @classmethod
    def get_user_tags_list(cls, user_id: str) :
        query = "SELECT tag_id FROM user_interests WHERE user_id = %s"
        rows = cls._fetch(query, (user_id,))
        return rows
    
    @classmethod
    def get_user_tag_existance(cls, user_id: str, tag_id: str) :
        query = "SELECT tag_id FROM user_interests WHERE user_id = %s AND tag_id = %s"
        row = cls._fetch_one(query, (user_id, tag_id,))
        return (row is not None)
    
        