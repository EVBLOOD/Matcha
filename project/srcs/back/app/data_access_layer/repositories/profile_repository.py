from data_access_layer.base_repository import BaseRepository
from data_access_layer.models.profile import Profile

class ProfileRepository(BaseRepository):
    _table_name = "profiles"
    _columns = [
        "user_id", "gender", 
        "sexual_preference", "biography",
        "location_set_by_user"
    ]

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
        """
        params = (
            profile.user_id,
            profile.gender,
            profile.sexual_preference,
            profile.biography,
            profile.location_set_by_user
        )
        return cls._execute(query, params) > 0