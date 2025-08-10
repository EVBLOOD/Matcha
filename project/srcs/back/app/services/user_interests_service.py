from app.dal.repositories.user_interests_repository import UserInterestsRepository, UserInterests
from app.dal.repositories.user_interests_repository import UserInterests, UserInterestsRepository

class UserInterestsService:
    @staticmethod
    def insert_user_interests(tag_id: int, user_id: int) :
        UserInterestsRepository.create_user_interests(
            UserInterests(user_id, tag_id)  )

    @staticmethod
    def check_user_interest_relation(tag_id: int, user_id: int) :
        if UserInterestsRepository.get_user_tag_existance(user_id, tag_id) :
            raise ValueError("Tag isn't valid")
        
        UserInterestsRepository.create_user_interests(
            UserInterests(user_id, tag_id)
        )
        