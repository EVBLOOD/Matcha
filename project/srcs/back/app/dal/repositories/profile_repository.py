from app.dal.base_repository import BaseRepository
from app.dal.models.profile import Profile

class ProfileRepository(BaseRepository):
    _table_name = "profiles"
    _columns = [
        "user_id", "gender", 
        "sexual_preference", "biography",
        "location_set_by_user"
    ]
        # query = """
        #     UPDATE users 
        #     SET verification_token = %s 
        #     WHERE id = %s
        #     RETURNING id
        # """
    @classmethod
    def upsert_profile(cls, profile: Profile) -> bool:
        query = """
            INSERT INTO profiles 
            (user_id, gender, sexual_preference, biography, location_set_by_user)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                gender = EXCLUDED.gender,
                sexual_preference = EXCLUDED.sexual_preference,
                biography = EXCLUDED.biography,
                location_set_by_user = EXCLUDED.location_set_by_user
            RETURNING user_id
        """
        params = (
            profile.user_id,
            profile.gender,
            profile.sexual_preference,
            profile.biography,
            profile.location_set_by_user
        )
        return cls._execute(query, params)

    @classmethod
    def update_profile(cls, profile: Profile) -> bool:
        query = """
            UPDATE profiles 
            SET
                gender = %s,
                sexual_preference = %s,
                biography = %s
            WHERE user_id = %s
            RETURNING user_id
        """
        params = (
            profile.user_id,
            profile.gender,
            profile.sexual_preference,
            profile.biography
        )
        return cls._execute(query, params)


    @classmethod
    def find_profile_exists(cls, user_id: str) -> bool :
        return cls.find_by_something(id=user_id, something="user_id", what="user_id") != None
        