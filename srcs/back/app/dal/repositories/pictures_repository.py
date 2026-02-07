from app.dal.base_repository import BaseRepository
from app.dal.models.picture import Picture
from typing import Optional

class PicturesRepository(BaseRepository):
    _table_name = "user_pictures"
    _columns = [
        "id", "user_id", "url", "is_profile_picture"
    ]
    _columns_insertion = [
        "user_id", "url", "is_profile_picture"
    ]

    @classmethod
    def insert_picture(cls, profile_data: Picture, injected_cursor = None) :
        norm_data = {
            'user_id' : profile_data.user_id,
            'url' : profile_data.url,
            'is_profile_picture' : profile_data.is_profile_picture
        }
        picture_id = cls.insert(table_name=cls._table_name, columns=cls._columns_insertion, data=norm_data, injected_cursor=injected_cursor)
        return picture_id

    @classmethod
    def find_by_url_nd_user_id(cls, url: str, user_id: str) :
        query = "SELECT * FROM user_pictures WHERE url = %s AND user_id = %s"
        row = cls._fetch_one(query, (url, user_id, ))

        return Picture(*row) if row else None

    @classmethod
    def find_by_url(cls, url: str) :
        query = "SELECT * FROM user_pictures WHERE url = %s"
        row = cls._fetch_one(query, (url,))
        return Picture(*row) if row else None
    
    @classmethod
    def find_many_by_user_id(cls, user_id: int) :
        query = "SELECT * FROM user_pictures WHERE user_id = %s"
        rows = cls._fetch(query, (user_id,))
        return rows
    
    @classmethod
    def update_picture(cls, profile_data: Picture) :
        query = """
            UPDATE user_pictures 
            SET url = %s, is_profile_picture = %s 
            WHERE id = %s
        """
        return cls._execute(query, (profile_data.url, profile_data.is_profile_picture, profile_data.id, )) > 0

    @classmethod
    def update_picture_profile(cls, url: str, user_id: str, injected_cursor = None) :
        query = """
            UPDATE user_pictures 
            SET url = %s
            WHERE user_id = %s AND is_profile_picture = True RETURNING id
        """
        return cls._execute(query, (url, user_id, ), injected_cursor)