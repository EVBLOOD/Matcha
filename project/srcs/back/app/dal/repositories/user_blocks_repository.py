from app.dal.base_repository import BaseRepository
from app.dal.models.user_blocks import UserBlocks

class UserBlocksRepository(BaseRepository):
    _table_name = "user_blocks"
    _columns = [
        "blocker_id", "blocked_id", "created_at"
    ]
    _insert_columns = [
        "blocker_id", "blocked_id"
    ]
    @classmethod
    def create_user_blocks(cls, user_block: UserBlocks) :
        norm_data = {
            'blocker_id' : user_block.blocker_id,
            'blocked_id' : user_block.blocked_id,
        }
        blocker_id = cls.insert(table_name=cls._table_name, columns=cls._insert_columns, data=norm_data, returning="blocker_id")
        return blocker_id

    @classmethod
    def get_user_blocked_list(cls, user_id: int) :
        query = "SELECT blocked_id FROM user_blocks WHERE blocker_id = %s"
        rows = cls._fetch(query, (user_id,))
        return rows

    @classmethod
    def get_user_blockers_list(cls, user_id: int) :
        query = "SELECT blocker_id FROM user_blocks WHERE blocked_id = %s"
        rows = cls._fetch(query, (user_id,))
        return rows
    
    @classmethod
    def get_user_blocks_existance(cls, blocker_id: int, blocked_id: int) :
        query = "SELECT blocker_id FROM user_blocks WHERE blocker_id = %s AND blocked_id = %s"
        row = cls._fetch_one(query, (blocker_id, blocked_id,))
        return row

    @classmethod
    def get_user_blocks_existance_visca(cls, blocker_id: int, blocked_id: int) :
        query = "SELECT blocker_id FROM user_blocks WHERE (blocker_id = %s AND blocked_id = %s) OR (blocker_id = %s AND blocked_id = %s)"
        row = cls._fetch_one(query, (blocker_id, blocked_id, blocked_id,blocker_id ))
        return row

    @classmethod
    def remove_user_blocks_existance(cls, blocker_id: int, blocked_id: int) :
        blocker_id = cls.get_user_blocks_existance(blocker_id, blocked_id)
        if not blocker_id :
            return None
        return cls.delete((blocker_id, blocked_id))
