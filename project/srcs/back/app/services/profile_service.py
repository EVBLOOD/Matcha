from app.dal.models.profile import Profile
from app.dal.repositories.profile_repository import ProfileRepository
from app.services.tags_service import TagsService
# from app.dal.repositories.tags_repository import TagsRepository
from app.services.picture_service import PictureService
from app.services.auth_service import AuthService
from typing import Set

class ProfileService:
    @staticmethod
    def create_profile(user_id: int, gender: str, sexual_preference: str,\
                        biography: str, location_set_by_user: bool, latitude: float, longitude: float, files_list, tags: Set[str]) :
        if gender not in ('male', 'female', 'other') \
            or sexual_preference not in ('straight', 'gay', 'bisexual') \
                or not isinstance(bool(location_set_by_user), bool):
            raise ValueError("Form error inputs!")
        if ProfileRepository.find_profile_exists(user_id) :
            raise ValueError("Profile already filled!")
        if not files_list or len(files_list) > 5 or len(files_list) < 1:
            raise ValueError("Must provide 1-5 pictures")
        TagsService.check_tag_name_valid(tags)
        TagsService.insert_tags(tags, user_id)
        PictureService.proccess_images(files_list, user_id)
        was_done = ProfileRepository.upsert_profile(
            Profile(user_id, gender, sexual_preference, biography, location_set_by_user)
        )
        AuthService.update_profile_profile_completion(user_id)
        return was_done
    
    @staticmethod
    def update_profile(user_id: int, gender: str, sexual_preference: str,\
                        biography: str, location_set_by_user: bool, latitude: float, longitude: float) :
        if gender not in ('male', 'female', 'other') \
            or sexual_preference not in ('straight', 'gay', 'bisexual') \
                or not isinstance(location_set_by_user, bool):
            raise ValueError("Form error inputs!")

        return ProfileRepository.update_profile(
            Profile(user_id, gender, sexual_preference, biography)
        )

    @staticmethod
    def check_profile_filled(user_id: int) :
        return ProfileRepository.find_profile_exists(user_id)
