from app.core.config import Config
from app.dal.repositories.suggestions_repository import SuggestionsRepository
from app.services.profile_service import ProfileService


class SuggestionsService :
    @classmethod
    def get_suggestions(cls, user_id: str, filter: str, sort: str) :
        users = SuggestionsRepository.get_suggestions(user_id, filter, sort)
        if not users :
            return []
        suggestions = []
        for user in users :
            if user["location_set_by_user"] :
                city, country = ProfileService.get_user_address(user["latitude"], user["longitude"])
            else :
                Address = "Not Shared!"
            tmp = {
                "user_id": user["id"],
                "username": user["username"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "profile_picture_url": user["profile_picture_url"],
                "age": user["age"],
                "fame_rating": round(min(5, max(0, (user["fame_rating"] / 5000) * 4 + 1)), 1),
                "location": Address if not user["location_set_by_user"] else f"{city}, {country}"
            }
            suggestions.append(tmp)
        return suggestions
    
    @classmethod
    def get_emptyResearch(cls, user_id: str) :
        users = SuggestionsRepository.get_emptyResearch(user_id)
        research = []
        for user in users :
            if user["location_set_by_user"] :
                city, country = ProfileService.get_user_address(user["latitude"], user["longitude"])
            else :
                Address = "Not Shared!"
            tmp = {
                "user_id": user["id"],
                "is_liked": user["is_liked"],
                "username": user["username"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "profile_picture_url": user["profile_picture_url"],
                "age": user["age"],
                "fame_rating": round(min(5, max(0, (user["fame_rating"] / 5000) * 4 + 1)), 1),
                "location": Address if not user["location_set_by_user"] else f"{city}, {country}"
            }
            research.append(tmp)
        return research



    @classmethod
    def get_Research(cls, user_id: int, args: dict, sort_by: str):
        params = [user_id]

        query_body = """
            WITH currentuser AS (
                SELECT u.id, u.latitude, u.longitude, p.gender, 
                    COALESCE(p.sexual_preference, 'bisexual') as pref
                FROM users u JOIN profiles p ON u.id = p.user_id WHERE u.id = %s
            )
            SELECT 
                u.id, u.username, u.first_name, u.last_name, u.fame_rating,
                u.latitude, u.longitude, p.location_set_by_user,
                EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) AS age,
                (SELECT COUNT(*) FROM user_interactions ui WHERE ui.liker_id = cud.id AND ui.liked_id = u.id) as is_liked,
                (6371 * acos(cos(radians(cud.latitude)) * cos(radians(u.latitude)) * cos(radians(u.longitude) - radians(cud.longitude)) + sin(radians(cud.latitude)) * sin(radians(u.latitude)))) AS distance,
                (SELECT COUNT(*) FROM user_interests ui WHERE ui.user_id = u.id AND ui.tag_id IN (SELECT tag_id FROM user_interests WHERE user_id = cud.id)) as same_tags,
                (SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture)) FROM user_pictures up WHERE up.user_id = u.id AND up.is_profile_picture = TRUE) AS profile_picture_url
            FROM users u
            JOIN profiles p ON u.id = p.user_id
            CROSS JOIN currentuser cud
            WHERE u.id != cud.id
            AND u.id NOT IN (SELECT blocked_id FROM user_blocks WHERE blocker_id = cud.id)
            AND u.id NOT IN (SELECT blocker_id FROM user_blocks WHERE blocked_id = cud.id)
            AND EXISTS (SELECT 1 FROM user_pictures WHERE user_id = u.id AND is_profile_picture = TRUE)
            AND (
                    (cud.pref = 'bisexual') OR
                    (cud.pref = 'straight' AND p.gender != cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('straight', 'bisexual')) OR
                    (cud.pref = 'gay' AND p.gender = cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('gay', 'bisexual'))
            )
        """

        if args.get('age_min'):
            query_body += " AND EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) >= %s"; params.append(args['age_min'])
        if args.get('age_max'):
            query_body += " AND EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) <= %s"; params.append(args['age_max'])
        if args.get('fame_min'):
            raw_rating = max(0,(float(args['fame_min']) - 1) * (5000 / 4))
            query_body += " AND u.fame_rating >= %s"; params.append(int(raw_rating))
        if args.get('location'):
            query_body += " AND (6371 * acos(cos(radians(cud.latitude)) * cos(radians(u.latitude)) * cos(radians(u.longitude) - radians(cud.longitude)) + sin(radians(cud.latitude)) * sin(radians(u.latitude)))) <= %s"; params.append(args['location'])
        
        if args.get('tags'):
            tags = args.get('tags').split(',')

            placeholders = ", ".join(["%s"] * len(tags))
            
            query_body += f""" 
                AND u.id IN (
                    SELECT ui.user_id 
                    FROM user_interests ui 
                    JOIN tags t ON ui.tag_id = t.id 
                    WHERE t.name IN ({placeholders})
                )
            """

            params.extend(tags)
        
        sort_map = {
            "age": "age ASC",
            "location": "distance ASC",
            "fame": "u.fame_rating DESC", 
            "tags": "same_tags DESC",
            "default": "distance ASC, same_tags DESC, u.fame_rating DESC"
        }
        order_clause = sort_map.get(sort_by, sort_map["default"])

        users = SuggestionsRepository._fetch_all(f"{query_body} ORDER BY {order_clause}, u.id ASC LIMIT 20", params)

        if not users :
            users = []

        research = []
        for user in users:
            address = "Not Shared!"
            if user["location_set_by_user"]:
                try:
                    city, country = ProfileService.get_user_address(user["latitude"], user["longitude"])
                    address = f"{city}, {country}"
                except:
                    address = "Unknown Location"
            
            fame_score = round(min(5, max(0, (user["fame_rating"] / 5000) * 4 + 1)), 1)
            
            research.append({
                "user_id": user["id"],
                "username": user["username"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "profile_picture_url": user["profile_picture_url"],
                "age": user["age"],
                "fame_rating": fame_score,
                "location": address,
                "distance": round(user["distance"], 2),
                "is_liked": user["is_liked"]
            })

        return research
        

