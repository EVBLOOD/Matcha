from app.dal.models.notifications import Notification
from app.dal.repositories.notification_repository import notificationsRepository



class NotificationService:
    @staticmethod
    def create_notification(user_id: int, type: str, source_user_id: int):
        try :
            was_done = notificationsRepository.insert_notifications(
                Notification(user_id=user_id, type=type, source_user_id=source_user_id)
            )
        except Exception as e:
            raise Exception(e)
        return was_done
    
    @staticmethod
    def update_notification(id: int, user_id: str) :
        notif = notificationsRepository.find_by_id(id)
        if notif and notif.user_id :
            return notificationsRepository.update_notifications(Notification(user_id=user_id, id=id, is_read=True))
        return None
    
    
    @staticmethod
    def get_notifications(user_id: int) :
        try :
            data = notificationsRepository.get_user_notifications(user_id)
            notificationsRepository.update_notifications_all(user_id)
            return data
        except Exception as e :
            raise Exception(e)
        
    @staticmethod
    def get_number_unreaded_notification(user_id: int) :
        try :
            return notificationsRepository.get_number_unreaded_notification(user_id)
        except Exception as e :
            raise Exception(e)