from app.dal.base_repository import BaseRepository

class SuggestionsRepository(BaseRepository):
    
    @classmethod
    def get_suggestions(cls, user_id: int) :  # TODO: this is worng but keep for now
        query = """
            WITH currentuser AS (
                SELECT u.id, u.latitude, u.longitude, p.gender, p.sexual_preference
                FROM users u 
                JOIN profiles p ON u.id = p.user_id 
                WHERE u.id = 11
            )
            SELECT 
                u.id, u.username, u.fame_rating,
                (6371 * acos(cos(radians(cud.latitude)) * cos(radians(u.latitude)) * cos(radians(u.longitude) - radians(cud.longitude)) + 
                 sin(radians(cud.latitude)) * sin(radians(u.latitude)))) AS distance,
                (SELECT COUNT(*) FROM user_interests ui 
                 WHERE ui.user_id = u.id 
                 AND ui.tag_id IN (SELECT tag_id FROM user_interests WHERE user_id = cud.id)) as same_tags
            FROM users u
            JOIN profiles p ON u.id = p.user_id
            CROSS JOIN currentuser cud
            WHERE u.id != cud.id
              AND EXISTS (SELECT 1 FROM user_pictures WHERE user_id = cud.id AND is_profile_picture = TRUE)
              AND (
                (cud.sexual_preference = 'straight' AND p.gender != cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('straight', 'bisexual')) OR
                (cud.sexual_preference = 'gay' AND p.gender = cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('gay', 'bisexual')) OR
                (cud.sexual_preference = 'bisexual' AND (
                    (p.gender != cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('straight', 'bisexual')) OR
                    (p.gender = cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('gay', 'bisexual'))
                ))
              )
              AND u.id NOT IN (SELECT blocked_id FROM user_blocks WHERE blocker_id = cud.id)
            ORDER BY 
                distance ASC,
                same_tags DESC,
                u.fame_rating DESC
            LIMIT 50;
            """
        params = (user_id, user_id,user_id)
        return cls._fetch_all(query, params)