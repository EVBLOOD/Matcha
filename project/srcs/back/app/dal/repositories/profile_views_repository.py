from app.dal.base_repository import BaseRepository
from app.dal.models.profile_views import ProfileViews

class ProfileViewsRepository(BaseRepository):
    _table_name = "profile_views"
    _columns = [
        "id", "viewer_id", "viewed_id", "viewed_at"
    ]
    _insert_columns = [
        "viewer_id", "viewed_id"
    ]
    @classmethod
    def create_profile_views(cls, profile_view: ProfileViews) :
        norm_data = {
            'viewer_id' : profile_view.viewer_id,
            'viewed_id' : profile_view.viewed_id,
        }
        id = cls.insert(table_name=cls._table_name, columns=cls._insert_columns, data=norm_data, returning="id")
        return id

    @classmethod
    def get_user_liked_list(cls, user_id: int) :
        query = "SELECT viewed_id FROM profile_views WHERE viewer_id = %s"
        rows = cls._fetch(query, (user_id,))
        return rows

    @classmethod
    def get_user_likers_list(cls, user_id: int) :
        query = "SELECT viewer_id FROM profile_views WHERE viewed_id = %s"
        rows = cls._fetch(query, (user_id,))
        return rows
    
    @classmethod
    def get_profile_view_existance(cls, viewer_id: int, viewed_id: int) :
        query = "SELECT id FROM profile_views WHERE viewer_id = %s AND viewed_id = %s"
        row = cls._fetch_one(query, (viewer_id, viewed_id,))
        return row
    
    @classmethod
    def remove_profile_view_existance(cls, viewer_id: int, viewed_id: int) :
        id = cls.get_profile_view_existance(viewer_id, viewed_id)
        if not id :
            return None
        return cls.delete(id)
