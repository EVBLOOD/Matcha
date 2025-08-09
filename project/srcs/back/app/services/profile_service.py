from app.dal.models.profile import Profile
from app.dal.repositories.profile_repository import ProfileRepository
from app.services.picture_service import PictureService
from typing import Optional

class ProfileService:
    @staticmethod
    def create_profile(user_id: int, gender: str, sexual_preference: str,\
                        biography: str, location_set_by_user: bool, latitude: float, longitude: float, files_list) :
        if gender not in ('male', 'female', 'other') \
            or sexual_preference not in ('straight', 'gay', 'bisexual') \
                or not isinstance(bool(location_set_by_user), bool):
            raise ValueError("Form error inputs!")
        if ProfileRepository.find_profile_exists(user_id) :
            raise ValueError("Profile already filled!")
        if not files_list or len(files_list) > 5:
            raise ValueError("Must provide 1-5 pictures")
        PictureService.proccess_images(files_list, user_id)
        return ProfileRepository.upsert_profile(
            Profile(user_id, gender, sexual_preference, biography, location_set_by_user)
        )
    
    @staticmethod
    def update_profile(user_id: int, gender: str, sexual_preference: str,\
                        biography: str, location_set_by_user: bool, latitude: float, longitude: float) :
        if gender not in ('male', 'female', 'other') \
            or sexual_preference not in ('straight', 'gay', 'bisexual') \
                or not isinstance(location_set_by_user, bool):
            raise ValueError("Form error inputs!")
        if not ProfileRepository.find_profile_exists(user_id) :
            raise ValueError("Profile not even filled yet!")

        return ProfileRepository.upsert_profile(
            Profile(user_id, gender, sexual_preference, biography, location_set_by_user)
        )

    @staticmethod
    def check_profile_filled(user_id: int) :
        return ProfileRepository.find_profile_exists(user_id)
