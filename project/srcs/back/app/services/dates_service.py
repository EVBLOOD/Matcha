from datetime import datetime, timezone
from app.dal.repositories.user_repository import UserRepository
from app.services.user_interactions_service import UserInteractionsService
from app.dal.repositories.user_repository import BaseRepository

class DatesService:
    @staticmethod
    def propose_date(proposer_id: int, partner_id: int, location: str, 
                     datetime_str: str, description: str):

        if not UserInteractionsService.are_users_connected(proposer_id, partner_id):
            raise ValueError("You must be matched to propose a date")
        
        print(datetime_str, flush=True)
        try:
            scheduled_at = datetime.fromisoformat(datetime_str)
            if scheduled_at.tzinfo is None:
                scheduled_at = scheduled_at.replace(tzinfo=timezone.utc)
        except:
            raise ValueError("Invalid datetime format")
        
        if scheduled_at < datetime.now(timezone.utc):
            raise ValueError("Cannot schedule dates in the past")
        
        query = """
            INSERT INTO dates (proposer_id, partner_id, location, scheduled_at, description)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        result = BaseRepository._execute(query, (
            proposer_id, partner_id, location, scheduled_at, description
        ))

        # I should notif and save it
        
        return result['id']
    
    @staticmethod
    def respond_to_date(date_id: int, responder_id: int, status: str):
        if status not in ['accepted', 'declined']:
            raise ValueError("Invalid status")
                
        query = "SELECT partner_id FROM dates WHERE id = %s"
        date_info = BaseRepository._fetch_one(query, (date_id,))
        print("date_info", flush=True)
        
        if not date_info or date_info[0] != responder_id:
            raise ValueError("Unauthorized")
        print("date_info", flush=True)
        
        update_query = "UPDATE dates SET status = %s WHERE id = %s RETURNING id"
        BaseRepository._execute(update_query, (status, date_id))
    
    @staticmethod
    def get_user_dates(user_id: int):
        # query = """
        #     SELECT 
        #         d.id, d.location, d.scheduled_at, d.description, d.status,
        #         d.proposer_id, d.partner_id,
        #         CASE 
        #             WHEN d.proposer_id = %s THEN u2.username
        #             ELSE u1.username
        #         END as partner_username
        #     FROM dates d
        #     JOIN users u1 ON d.proposer_id = u1.id
        #     JOIN users u2 ON d.partner_id = u2.id
        #     WHERE d.proposer_id = %s OR d.partner_id = %s
        #     ORDER BY d.scheduled_at DESC
        # """

        query = """
            SELECT 
                d.id,
                d.location,
                d.scheduled_at,
                d.description,
                d.status,
                u1.username as proposer_username,
                u2.username as partner_username,
                d.proposer_id, d.partner_id,
                (
                    SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture))
                    FROM user_pictures up
                    WHERE up.user_id = u1.id AND is_profile_picture = TRUE
                ) AS proposer_avatar,
                (
                    SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture))
                    FROM user_pictures up
                    WHERE up.user_id = u2.id AND is_profile_picture = TRUE
                ) AS proposer_avatar
            FROM dates d
            JOIN users u1 ON d.proposer_id = u1.id
            JOIN users u2 ON d.partner_id = u2.id
            WHERE d.proposer_id = %s OR d.partner_id = %s
            ORDER BY d.scheduled_at DESC
        """
        
        return BaseRepository._fetch_all(query, (user_id, user_id))
