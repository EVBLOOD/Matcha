from app.core.config import Config
from app.dal.repositories.suggestions_repository import SuggestionsRepository
from app.services.profile_service import ProfileService
from app.dal.models.message import Message
from app.dal.models.conversation import Conversation

class SuggestionsService :
    @classmethod
    def get_suggestions(cls, user_id: str) :
        users = SuggestionsRepository.get_suggestions(user_id)
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
    def get_Research(cls, user_id: str, filters, sort_by: str, page) :
        search_query = """
                u.id NOT IN (SELECT blocked_id FROM user_blocks WHERE blocker_id = cud.id)
                AND u.id NOT IN (SELECT blocker_id FROM user_blocks WHERE blocked_id = cud.id)
                AND (
                    (cud.sexual_preference = 'straight' AND p.gender != cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('straight', 'bisexual')) OR
                    (cud.sexual_preference = 'gay' AND p.gender = cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('gay', 'bisexual')) OR
                    (cud.sexual_preference = 'bisexual' AND (
                        (p.gender != cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('straight', 'bisexual')) OR
                        (p.gender = cud.gender AND COALESCE(p.sexual_preference, 'bisexual') IN ('gay', 'bisexual'))
                    ))
                )
            """
        params = [user_id]
        if filters.get('age_min'):
            search_query += " AND EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) >= %s"
            params.append(filters['age_min'])

        if filters.get('age_max'):
            query += " AND EXTRACT(YEAR FROM AGE(NOW(), u.birthdate)) <= %s"
            params.append(filters['age_max'])

        if filters.get('fame_min'):
            query += " AND u.fame_rating >= %s"
            params.append(filters['fame_min'])

        if filters.get('location'): # list of cities
            print("this is to add -!", flush=True)

        if filters.get('tags'):
            tmp = ', '.join(['%s'] * len(filters['tags']))
            query += f""" AND u.id IN (
                SELECT ui.user_id FROM user_interests ui 
                JOIN tags t ON ui.tag_id = t.id 
                WHERE t.name IN ({tmp})
            )"""
            params.extend(filters['tags'])

        sort_options = {
            "age": "age ASC",
            "fame": "u.fame_rating DESC",
            "location": "distance ASC",
            "tags": "same_tags DESC"
        }


        
        order_clause = sort_options.get(sort_by, "distance ASC, same_tags DESC, u.fame_rating DESC")
        query += f" ORDER BY {order_clause}, u.id ASC LIMIT 20"
        users = SuggestionsRepository.get_Research(user_id)
        research = []
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
            research.append(tmp)
        return research