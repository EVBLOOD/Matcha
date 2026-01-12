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
