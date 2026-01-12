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
    def get_user_profile(cls, user_id: str, same: bool, my_acount: str = "") -> bool :
        if same :
            query = """
                SELECT
                    u.id AS user_id,
                    u.username,
                    u.first_name,
                    u.last_name,
                    u.fame_rating,
                    u.last_online,
                    u.latitude,
                    u.longitude,
                    p.gender,
                    p.sexual_preference,
                    p.biography,
                    p.location_set_by_user,
                    EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) AS age,
                    (
                        SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture))
                        FROM user_pictures up
                        WHERE up.user_id = u.id
                    ) AS profile_picture_url,
                    (
                        SELECT json_agg(t.name)
                        FROM user_interests ui
                        JOIN tags t ON ui.tag_id = t.id
                        WHERE ui.user_id = u.id
                    ) AS interests,
                    (SELECT COUNT(*) FROM user_interactions WHERE liked_id = u.id AND status = 'liked') AS likes_count,
                    (SELECT COUNT(*) FROM profile_views WHERE viewed_id = u.id) AS views_count
                FROM users u
                LEFT JOIN profiles p ON u.id = p.user_id
                WHERE
                    u.id = %s;
            """
            params = (user_id, )

        else :
            query = """
                SELECT
                    u.id as user_id,
                    u.username,
                    u.first_name,
                    u.fame_rating,
                    u.last_name,
                    u.longitude,
                    u.latitude,
                    p.gender,
                    p.sexual_preference,
                    p.biography,
                    p.location_set_by_user,
                    EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) AS age,
                    (
                        SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture))
                        FROM user_pictures up
                        WHERE up.user_id = u.id
                    ) AS profile_picture_url,
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
                        WHERE (liker_id = %s AND liked_id = u.id) OR (liker_id = u.id AND liked_id = %s) AND status = 'liked'
                    ) AS is_connected,
                    (SELECT COUNT(*) FROM user_interactions WHERE liked_id = u.id AND status = 'liked') AS likes_count,
                    (SELECT COUNT(*) FROM profile_views WHERE viewed_id = u.id) AS views_count,
                    (SELECT COUNT(*) FROM user_blocks WHERE (blocker_id = u.id AND blocker_id = %s) OR (blocker_id = %s AND blocker_id = u.id)) AS user_block_status,
                    (SELECT id FROM conversations WHERE (user1_id = u.id AND user2_id = %s) OR (user1_id = %s AND user2_id = u.id)) AS converstion_id

                FROM
                    users AS u
                JOIN
                    profiles AS p ON u.id = p.user_id
                JOIN
                    user_pictures AS up ON u.id = up.user_id
                WHERE
                    u.id = %s;
            """
            params = (my_acount, my_acount, my_acount, user_id, user_id,my_acount, my_acount, user_id,)

        return cls._execute(query, params)
