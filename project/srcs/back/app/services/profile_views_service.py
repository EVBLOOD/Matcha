from app.dal.repositories.profile_views_repository \
    import ProfileViews,ProfileViewsRepository

from app.dal.repositories.user_repository import UserRepository

class ProfileViewsService:
    
    @staticmethod
    def insert_profile_views(viewed_id: int, user_id: int) :
        if not UserRepository.find_by_id(viewed_id) :
            raise ValueError("User doesn't exist!")

        interact = ProfileViews(viewed_id=viewed_id, viewer_id=user_id)

        ProfileViewsRepository.create_profile_views(interact)

    @staticmethod
    def get_profile_views(viewed_id: int, user_id: int) :
        if not UserRepository.find_by_id(viewed_id) :
            raise ValueError("User doesn't exist!")

        row = ProfileViewsRepository.get_profile_view_existance(user_id, viewed_id)
        return row


    @staticmethod
    def remove_profile_views(viewed_id: int, user_id: int) :
        if not UserRepository.find_by_id(viewed_id) :
            raise ValueError("User doesn't exist!")

        return ProfileViewsRepository.remove_profile_view_existance(viewed_id=viewed_id, 
                                                                     viewer_id=user_id)
    
    def get_all_likes_got(user_id: int = None, viewed_id: int = None) :
        get_likes = None
        if user_id :
            get_likes = user_id
        else :
            if not UserRepository.find_by_id(viewed_id) :
                raise ValueError("User doesn't exist!")
            get_likes = viewed_id
        return ProfileViewsRepository.get_user_likers_list(get_likes)

    def get_all_ot_likes_given(user_id: int = None, viewed_id: int = None) :
        get_likes = None
        if user_id :
            get_likes = user_id
        else :
            if not UserRepository.find_by_id(viewed_id) :
                raise ValueError("User doesn't exist!")
            get_likes = viewed_id
        return ProfileViewsRepository.get_user_liked_list(get_likes)
    