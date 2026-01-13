from app.dal.repositories.user_blocks_repository \
    import UserBlocks,UserBlocksRepository

from app.dal.repositories.user_repository import UserRepository

class UserBlocksService:
    
    @staticmethod
    def insert_user_blocks(blocked_id: int, user_id: int) :
        if not UserRepository.find_by_id(blocked_id) :
            raise ValueError("User doesn't exist!")
        interact = UserBlocks(blocked_id=blocked_id, blocker_id=user_id)

        UserBlocksRepository.create_user_blocks(interact)

    @staticmethod
    def get_user_blocks(blocked_id: int, user_id: int) :
        if not UserRepository.find_by_id(blocked_id) :
            raise ValueError("User doesn't exist!")

        row = UserBlocksRepository.get_user_blocks_existance(user_id, blocked_id)
        return row


    @staticmethod
    def remove_user_blocks(blocked_id: int, user_id: int) :
        if not UserRepository.find_by_id(blocked_id) :
            raise ValueError("User doesn't exist!")

        return UserBlocksRepository.remove_user_blocks_existance(blocked_id=blocked_id, 
                                                                     blocker_id=user_id)

    def get_blocks_status(user_id: int, user_id_two: int) :
        return UserBlocksRepository.get_user_blocks_existance_visca(user_id, user_id_two)

    def get_all_blocks_got(user_id: int = None, blocked_id: int = None) :
        get_blocks = None
        if user_id :
            get_blocks = user_id
        else :
            if not UserRepository.find_by_id(blocked_id) :
                raise ValueError("User doesn't exist!")
            get_blocks = blocked_id
        return UserBlocksRepository.get_user_blockers_list(get_blocks)

    def get_all_ot_blocks_given(user_id: int = None, blocked_id: int = None) :
        get_blocks = None
        if user_id :
            get_blocks = user_id
        else :
            if not UserRepository.find_by_id(blocked_id) :
                raise ValueError("User doesn't exist!")
            get_blocks = blocked_id
        return UserBlocksRepository.get_user_blocked_list(get_blocks)
    