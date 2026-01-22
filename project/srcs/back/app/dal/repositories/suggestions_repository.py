from app.dal.base_repository import BaseRepository

class SuggestionsRepository(BaseRepository):
    
    @classmethod
    def get_suggestions(cls, user_id: int, filter: str, sort: str):
        params = [user_id]

        query_base = """
            WITH currentuser AS (
                SELECT u.id, u.latitude, u.longitude, p.gender, 
                    COALESCE(p.sexual_preference, 'bisexual') as pref,
                    EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) as age
                FROM users u JOIN profiles p ON u.id = p.user_id WHERE u.id = %s
            )
            SELECT 
               u.id,
                u.username,
                u.fame_rating,
                u.first_name,
                u.last_name,
                u.latitude,
                u.longitude,
                EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) AS age,
                (SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture)) FROM user_pictures up WHERE up.user_id = u.id AND up.is_profile_picture = TRUE) AS profile_picture_url,
                (6371 * acos(cos(radians(cud.latitude)) * cos(radians(u.latitude)) * cos(radians(u.longitude) - radians(cud.longitude)) + sin(radians(cud.latitude)) * sin(radians(u.latitude)))) AS distance,
                (SELECT COUNT(*) FROM user_interests ui WHERE ui.user_id = u.id AND ui.tag_id IN (SELECT tag_id FROM user_interests WHERE user_id = cud.id)) as same_tags,
                p.location_set_by_user
            FROM users u
            JOIN profiles p ON u.id = p.user_id
            CROSS JOIN currentuser cud
            WHERE u.id != cud.id
            AND u.id NOT IN (
                SELECT liked_id 
                FROM user_interactions 
                WHERE liker_id = cud.id
            )
                    AND EXISTS (SELECT 1 FROM user_pictures WHERE user_id = u.id AND is_profile_picture = TRUE)
                    AND u.id NOT IN (SELECT blocked_id FROM user_blocks WHERE blocker_id = cud.id)
                    AND u.id NOT IN (SELECT blocker_id FROM user_blocks WHERE blocked_id = cud.id)
                    AND (
                        (cud.pref = 'bisexual') OR
                        (cud.pref = 'straight' AND p.gender != cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('straight', 'bisexual')) OR
                        (cud.pref = 'gay' AND p.gender = cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('gay', 'bisexual'))
                    )
        """
    
        if filter == "location":
            query_base += """ AND (
                6371 * acos(cos(radians(cud.latitude)) * cos(radians(u.latitude)) * cos(radians(u.longitude) - radians(cud.longitude)) + 
                sin(radians(cud.latitude)) * sin(radians(u.latitude)))
            ) < 50 """
        elif filter == "tags":
            query_base += " AND EXISTS (SELECT 1 FROM user_interests ui WHERE ui.user_id = u.id AND ui.tag_id IN (SELECT tag_id FROM user_interests WHERE user_id = cud.id))"
        elif filter == "fame":
            query_base += " AND u.fame_rating > 50"
        elif filter == "age":
            query_base += " AND EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) BETWEEN cud.age - 5 AND cud.age + 5"

        sort_map = {
            "age": "age ASC",
            "location": "distance ASC",
            "fame": "u.fame_rating DESC",
            "tags": "same_tags DESC",
            "default": "distance ASC, same_tags DESC, u.fame_rating DESC"
        }
        order_clause = sort_map.get(sort, sort_map["default"])
        
        final_query = f"{query_base} ORDER BY {order_clause} LIMIT 20"

        return cls._fetch_all(final_query, params)

    @classmethod
    def get_emptyResearch(cls, user_id: int) :
        query = """
            WITH currentuser AS (
                SELECT u.id, u.latitude, u.longitude, p.gender, p.sexual_preference
                FROM users u 
                JOIN profiles p ON u.id = p.user_id 
                WHERE u.id = %s
            )
            SELECT 
                u.id,
                u.username,
                u.fame_rating,
                u.first_name,
                u.last_name,
                u.latitude,
                u.longitude,
                EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) AS age,
                (SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture)) FROM user_pictures up WHERE up.user_id = u.id AND up.is_profile_picture = TRUE) AS profile_picture_url,
                (6371 * acos(cos(radians(cud.latitude)) * cos(radians(u.latitude)) * cos(radians(u.longitude) - radians(cud.longitude)) + sin(radians(cud.latitude)) * sin(radians(u.latitude)))) AS distance,
                (SELECT COUNT(*) FROM user_interests ui WHERE ui.user_id = u.id AND ui.tag_id IN (SELECT tag_id FROM user_interests WHERE user_id = cud.id)) as same_tags,
                p.location_set_by_user
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
              AND u.id NOT IN (SELECT blocker_id FROM user_blocks WHERE blocked_id = cud.id)
            ORDER BY 
                fame_rating 
                DESC
            LIMIT 20;
        """
        params = (user_id,)
        return cls._fetch_all(query, params)
    
    @classmethod
    def get_Research(cls, search_query, params) :
        query = f"""
                WITH currentuser AS (
                    SELECT id, latitude, longitude, gender, sexual_preference
                    FROM users u 
                    JOIN profiles p ON u.id = p.user_id 
                    WHERE u.id = %s
                )
                SELECT 
                    u.id, u.username, u.fame_rating, u.first_name, u.last_name,
                    u.latitude, u.longitude,
                    EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) AS age,
                    (SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture)) 
                     FROM user_pictures up WHERE up.user_id = u.id AND up.is_profile_picture = TRUE) AS profile_picture,
                    (6371 * acos(cos(radians(cud.latitude)) * cos(radians(u.latitude)) * cos(radians(u.longitude) - radians(cud.longitude)) + 
                     sin(radians(cud.latitude)) * sin(radians(u.latitude)))) AS distance,
                    (SELECT COUNT(*) FROM user_interests ui 
                     WHERE ui.user_id = u.id AND ui.tag_id IN 
                     (SELECT tag_id FROM user_interests WHERE user_id = cud.id)) as same_tags,
                    p.location_set_by_user
                    
                FROM users u
                JOIN profiles p ON u.id = p.user_id
                CROSS JOIN currentuser cud
                WHERE u.id != cud.id
                  AND {search_query}  LIMIT 20
            """
        
        rows = cls._fetch_all(query, params)
        
        # query = f"""
        #         WITH currentuser AS (
        #             SELECT id, latitude, longitude, gender, sexual_preference
        #             FROM users u 
        #             JOIN profiles p ON u.id = p.user_id 
        #             WHERE u.id = %s
        #         )
        #         SELECT 
        #             COUNT(u.id)
        #         FROM users u
        #         JOIN profiles p ON u.id = p.user_id
        #         CROSS JOIN currentuser cud
        #         WHERE u.id != cud.id
        #           AND {search_query}
        #     """
        # page_data = cls._fetch_one(query, params)
        
        return {"data": rows, "page": (20/ 20)}

# (SELECT COUNT(*) FROM user_blocks WHERE (blocked_id = u.id AND blocker_id = %s) OR (blocked_id = %s AND blocker_id = u.id)) AS user_block_status,