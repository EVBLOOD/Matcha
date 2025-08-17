from app.dal.base_repository import BaseRepository
from app.dal.models.profile import Profile

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
    
    @classmethod
    def get_user_profile(cls, user_id: str, my_acount = None) -> bool :
        if my_acount :
            query = """
                SELECT
                    u.id,
                    u.username,
                    u.first_name,
                    u.last_name,
                    u.email,
                    u.fame_rating,
                    u.latitude,
                    u.longitude,
                    p.gender,
                    p.sexual_preference,
                    p.biography,
                    p.location_set_by_user,
                    up.url AS profile_picture_url,
                    (SELECT COUNT(*) FROM user_interactions WHERE liked_id = u.id AND status = 'liked') AS likes_count,
                    (SELECT COUNT(*) FROM profile_views WHERE viewed_id = u.id) AS views_count
                FROM
                    users AS u
                JOIN
                    profiles AS p ON u.id = p.user_id
                LEFT JOIN
                    user_pictures AS up ON u.id = up.user_id AND up.is_profile_picture = TRUE
                WHERE
                    u.id = %s;
            """
            params = (user_id, )

        else : # TODO: I think I should add -> LOCATION too in this case
            query = """
                SELECT
                    u.id,
                    u.username,
                    u.first_name,
                    u.fame_rating,
                    p.gender,
                    p.sexual_preference,
                    p.biography,
                    up.url AS profile_picture_url,
                    (
                        SELECT array_agg(t.name)
                        FROM user_interests AS ui
                        JOIN tags AS t ON ui.tag_id = t.id
                        WHERE ui.user_id = u.id
                    ) AS interests,
                    (
                        SELECT status
                        FROM user_interactions
                        WHERE liker_id = %s AND liked_id = u.id
                    ) AS interaction_status,
                    (
                        SELECT count(*)
                        FROM user_interactions
                        WHERE (liker_id = %s AND liked_id = u.id) OR (liker_id = u.id AND liked_id = %s)
                    ) AS is_connected,
                    (SELECT COUNT(*) FROM user_interactions WHERE liked_id = u.id AND status = 'liked') AS likes_count
                FROM
                    users AS u
                JOIN
                    profiles AS p ON u.id = p.user_id
                JOIN
                    user_pictures AS up ON u.id = up.user_id AND up.is_profile_picture = TRUE
                WHERE
                    u.id = %s;
            """
            params = (my_acount, my_acount, user_id, )
        return cls._execute(query, params)
    

