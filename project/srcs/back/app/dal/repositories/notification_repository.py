from app.dal.base_repository import BaseRepository
from app.dal.models.notifications import Notification

class notificationsRepository(BaseRepository):
    _table_name = "notifications"
    _columns = [
        "user_id", "type", 
        "source_user_id", "is_read"
    ]
    @classmethod
    def insert_notifications(cls, notifications: Notification) -> bool:
        query = """
            INSERT INTO notifications
            (user_id, type, source_user_id)
            VALUES (%s, %s, %s)
            RETURNING user_id
        """
        params = (
            notifications.user_id,
            notifications.type,
            notifications.source_user_id
        )
        return cls._execute(query, params)

    @classmethod
    def update_notifications(cls, notifications: Notification) -> bool:
        query = """
            UPDATE notifications
            SET
                is_read = %s,
            WHERE id = %s
            RETURNING id
        """
        params = (
            notifications.is_read,
            notifications.id
        )
        return cls._execute(query, params)
    
    @classmethod
    def get_user_notifications(cls, user_id: str) -> bool :
        query = """
                SELECT
                    n.id AS notification_id,
                    n.user_id,
                    n.type,
                    n.source_user_id,
                    n.is_read,
                    n.created_at,
                    s.username,
                    (
                        SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture))
                        FROM user_pictures up
                        WHERE up.user_id = n.source_user_id AND is_profile_picture = TRUE
                    ) AS picture_url
                FROM notifications n
                LEFT JOIN users s ON n.source_user_id = s.id
                WHERE
                    n.user_id = %s
                ORDER BY created_at DESC
            """
        params = (user_id, )

        return cls._fetch_all(query, params)
    

    @classmethod
    def get_number_unreaded_notification(cls, user_id: str) :
        query = """
            SELECT
                COUNT(id)
            FROM notifications
            WHERE
                user_id = %s AND is_read = FALSE
        """
        params = (user_id, )

        return cls._fetch_one(query, params)
    
