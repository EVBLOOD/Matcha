from app.dal.repositories.user_interactions_repository \
    import UserInteractions,UserInteractionsRepository

from app.dal.repositories.user_repository import UserRepository

class UserInteractionsService:
    
    @staticmethod
    def insert_user_interactions(liked_user: int, user_id: int) :
        if not UserRepository.find_by_id(liked_user) :
            raise ValueError("User doesn't exist!")
        print(f"insert_user_interactions", flush=True)

        interact = UserInteractions(liked_id=liked_user, liker_id=user_id, status="liked")
        print(f"insert_user_interactions = interact =", flush=True)

        UserInteractionsRepository.create_user_interactions(interact)

    @staticmethod
    def get_user_interactions(liked_user: int, user_id: int) :
        if not UserRepository.find_by_id(liked_user) :
            raise ValueError("User doesn't exist!")
        row = UserInteractionsRepository.get_user_interaction_existance(user_id, liked_user)
        return row
    
    @staticmethod
    def are_users_connected(liked_user: int, user_id: int) :
        if not UserRepository.find_by_id(liked_user) :
            raise ValueError("User doesn't exist!")
        return UserInteractionsRepository.are_users_connected(user_id, liked_user)
    


    @staticmethod
    def remove_user_interactions(liked_user: int, user_id: int) :
        if not UserRepository.find_by_id(liked_user) :
            raise ValueError("User doesn't exist!")
        return UserInteractionsRepository.remove_user_interaction_existance(liked_id=liked_user, 
                                                                     liker_id=user_id)
    
    def get_all_likes_got(user_id: int = None, liked_user: int = None) :
        get_likes = None
        if user_id :
            get_likes = user_id
        else :
            if not UserRepository.find_by_id(liked_user) :
                raise ValueError("User doesn't exist!")
            get_likes = liked_user
        return UserInteractionsRepository.get_user_likers_list(get_likes)

    def get_all_ot_likes_given(user_id: int = None, liked_user: int = None) :
        get_likes = None
        if user_id :
            get_likes = user_id
        else :
            if not UserRepository.find_by_id(liked_user) :
                raise ValueError("User doesn't exist!")
            get_likes = liked_user
        return UserInteractionsRepository.get_user_liked_list(get_likes)
    