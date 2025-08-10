from app.dal.repositories.tags_repository import TagsRepository, Tags
from app.dal.repositories.user_interests_repository import UserInterests, UserInterestsRepository
from typing import Set

# from app.services.picture_service import PictureService
# from app.services.auth_service import AuthService
# from typing import Optional
import re
class TagsService:
    @staticmethod
    def insert_tags(tags: Set[str], user_id: str) :

        for tag in tags :
            id_tag = TagsRepository.find_tags_exists(
                tag_name=tag
            )
            if id_tag is None :
                tag_id = TagsRepository.create_tags(
                    Tags(id=0, name=tag)
                )
            UserInterestsRepository.create_user_interests( 
                UserInterests(user_id=int(user_id), tag_id=tag_id)
            )
    def check_tag_name_valid(tags : Set[str]) :
        if not isinstance(tags, Set):
            raise ValueError("Form error inputs!")
        for tag in tags :
            if not re.fullmatch(r'^#[\wÀ-ÿ\- ]{1,29}$', tag, re.UNICODE) :
                raise ValueError("Tag isn't valid")
