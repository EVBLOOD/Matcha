from app.dal.repositories.user_repository import UserRepository
from app.dal.base_repository import BaseRepository

class ReportService(BaseRepository):
    @classmethod
    def report_user(cls, reporter_id: int, reported_id: int, reason: str):        
        if reporter_id == reported_id:
            raise ValueError("Cannot report yourself")
        
        if not UserRepository.find_by_id(reported_id):
            raise ValueError("User doesn't exist")
        
        query = """
            SELECT id FROM user_reports 
            WHERE reporter_id = %s AND reported_id = %s
        """
        existing = cls._fetch_one(query, (reporter_id, reported_id))
        
        if existing:
            raise ValueError("You already reported this user")

        query = """
            INSERT INTO user_reports (reporter_id, reported_id, reason)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        cls._execute(query, (reporter_id, reported_id, reason))
        
        query = """
            SELECT COUNT(*) FROM user_reports WHERE reported_id = %s
        """
        report_count = cls._fetch_one(query, (reported_id,))[0]
        
        if report_count >= 5:
            # TO BLOCK USER OR DELETE IT
            print(f"reported_id: {reported_id} report_count: {report_count}", flush=True)
        return True