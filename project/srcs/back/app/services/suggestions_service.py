from app.core.config import Config
from app.dal.repositories.suggestions_repository import SuggestionsRepository
from app.dal.models.message import Message
from app.dal.models.conversation import Conversation

class SuggestionsService :
    @classmethod
    def get_suggestionss(cls, user_id: str) :
        return SuggestionsRepository.get_suggestionss(user_id)