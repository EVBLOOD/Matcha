from app.dal.models.profile import Profile
from app.dal.repositories.profile_repository import ProfileRepository
from app.dal.repositories.user_repository import UserRepository
from app.services.user_interactions_service import UserInteractionsService
from app.services.user_interests_service import UserInterestsService

from app.services.tags_service import TagsService
# from app.dal.repositories.tags_repository import TagsRepository
from app.services.picture_service import PictureService
from app.services.auth_service import AuthService
from typing import Set

class ProfileService:
    # TODO:
    # this has a problem in case of failure of one of the insertions in the database, it should be fixed 
    # two solutions : remove everything in case of execption - just verify if the element is free then fill it
    # in that case
    @staticmethod
    def create_profile(user_id: int, gender: str, sexual_preference: str,\
                        biography: str, location_set_by_user: bool, files_list, tags: str, latitude: float = 0, longitude: float = 0) :
        
        tags_list = set(tags.split(';'))

        if ProfileRepository.find_profile_exists(user_id) :
            raise ValueError("Profile already filled!")
        if not files_list or len(files_list) > 5 or len(files_list) < 1:
            raise ValueError("Must provide 1-5 pictures")
        TagsService.check_tag_name_valid(tags_list) # TODO: trim tags
        try :
            TagsService.insert_tags(tags_list, user_id)
            PictureService.proccess_images(files_list, user_id)
            was_done = ProfileRepository.upsert_profile(
                Profile(user_id, gender, sexual_preference, biography, location_set_by_user)
            )
            AuthService.update_profile_profile_completion(user_id)
        except Exception as e:
            raise Exception(e)
        return was_done
    
    @staticmethod
    def update_profile(user_id: int, gender: str, sexual_preference: str,\
                        biography: str, location_set_by_user: bool, latitude: float, longitude: float) :
    # TODO: we should update this too location_set_by_user: bool, latitude: float, longitude: float
        return ProfileRepository.update_profile(
            Profile(user_id, gender, sexual_preference, biography)
        )

    @staticmethod
    def check_profile_filled(user_id: int) :
        return ProfileRepository.find_profile_exists(user_id)
    
    @staticmethod
    def get_profile(searcher_id: int, to_find_user_name: str) :
        try :
            user = UserRepository.find_by_username(to_find_user_name)
            if user.id == searcher_id :
                same = True
            profile = ProfileRepository.get_user_profile(user_id=user.id)
            
            iteraction_him = UserInteractionsService.get_all_likes_got(user_id = searcher_id, liked_user = user.id)
            iteraction_other = UserInteractionsService.get_all_ot_likes_given(user_id = user.id, liked_user = searcher_id)

            if iteraction_him and iteraction_other :
                relation = "match"
            elif iteraction_him :
                relation = "searcher liked him"
            elif iteraction_other :
                relation = "liked the searcher"
            else :
                relation = "NAN"
            tags = [(1, "#tags"), (2, "#tags")]
            # tags = UserInterestsService.get_user_interests(user_id = user.id)
            pictures = [("path1", True), ("path2", False), ("path3", False), ("path4", False)]
            if same :
                personal = {
                    "email": user.email
                }
            else :
                personal = None
            return {
                "user_id": 1,
                "relation": relation,
                "user_name": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "tags": tags,
                "pictures": pictures,
                "same": personal
            }
        except Exception as e :
            raise Exception(e)