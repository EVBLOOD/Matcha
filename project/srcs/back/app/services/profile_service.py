from app.dal.models.profile import Profile
from app.dal.repositories.profile_repository import ProfileRepository


from app.services.tags_service import TagsService
# from app.dal.repositories.tags_repository import TagsRepository
from app.dal.repositories.user_repository import UserRepository
from app.services.picture_service import PictureService
from app.services.auth_service import AuthService
from app.core.config import Config
# from typing import Set

from flask import jsonify
import requests

import geoip2.database

from geoip2.errors import AddressNotFoundError
import ipaddress



class ProfileService:
    # TODO:
    # this has a problem in case of failure of one of the insertions in the database, it should be fixed 
    # two solutions : remove everything in case of execption - just verify if the element is free then fill it
    # in that case
    @staticmethod
    def create_profile(user_id: int, gender: str, sexual_preference: str,\
                        biography: str, location_set_by_user: bool, files_list, tags: str, latitude: float = 0, longitude: float = 0, ip: str = "") :
        
        tags_list = set(tags.split(';'))
        if ProfileRepository.find_profile_exists(user_id) :
            raise ValueError("Profile already filled!")        
        if not files_list or len(files_list) > 5 or len(files_list) < 1:
            raise ValueError("Must provide 1-5 pictures")
        TagsService.check_tag_name_valid(tags_list) # TODO: trim tags
        try :
            TagsService.insert_tags(tags_list, user_id)
            PictureService.proccess_images(files_list, user_id)
            
            print(f"latitude: {latitude}, longitude: {longitude}", flush=True)
            print(f"not location_set_by_user {not location_set_by_user }")
            print(f"not (not latitude and not longitude) {(not latitude and not longitude)}")
            print(f"(-90 <= latitude <= 90 and -180 <= longitude <= 180) {(-90 <= latitude <= 90 and -180 <= longitude <= 180)}")
            print(f"not (-90 <= latitude <= 90 and -180 <= longitude <= 180) {not (-90 <= latitude <= 90 and -180 <= longitude <= 180)}")
            if not location_set_by_user or (not latitude and not longitude) or \
                not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                result = ProfileService.initial_location(ip)
                latitude = result["lat"]
                longitude = result["lng"]
            was_done = ProfileRepository.upsert_profile(
                Profile(user_id, gender, sexual_preference, biography, location_set_by_user)
            )
            UserRepository.update_location(user_id, latitude, longitude)
            AuthService.update_profile_profile_completion(user_id)
        except Exception as e:
            print(f"{e}", flush=True)
            raise Exception(e)
        return was_done

    @staticmethod
    def is_public_ip(ip):
        try:
            ip_obj = ipaddress.ip_address(ip)
            return ip_obj.is_global
        except ValueError:
            return False

    
    @staticmethod
    def initial_location(ip: str) :    
        if not ProfileService.is_public_ip(ip):
            ip = Config.PUBLIC_IP

        try:
            resp = Config.GEOIP_READER.city(ip)
            result = {
                "lat": resp.location.latitude,
                "lng": resp.location.longitude,
                "ip": ip
            }
            print(f"GEOIP_READER: {resp}", flush=True)
            print(f"result: {result}", flush=True)
            return result

        except AddressNotFoundError:
            print(f"Address {ip} not found in the database.",flush=True)
        except Exception as e:
            print(f"An error occurred: {e}", flush=True)

        return None

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
    def get_profile(searcher_id: int, to_find_user_id: int) :
        try :
            same = False
            if to_find_user_id== searcher_id :
                same = True
            profile = ProfileRepository.get_user_profile(user_id=to_find_user_id, my_acount=searcher_id, same=same)
            if profile is None : 
                raise ValueError("No such a profile")

            print(profile, flush=True)
            if same :
                interactions = {
                    "is_same": True,
                    "likes_count": profile["likes_count"],
                    "views_count": profile["views_count"]
                }
            else :
                if profile["user_block_status"] and profile["user_block_status"] > 0 :
                    raise ValueError("No such a profile")
                
                interactions = {
                    "is_same": False,
                    "interaction_status": profile["interaction_status"],
                    "is_connected": profile["is_connected"],
                    "likes_count": profile["likes_count"],
                    "views_count": profile["views_count"]
                }
                if profile["is_connected"] == 2:
                    lkd = profile["converstion_id"]
                    print(f"profile: is_connected : {lkd}", flush=True)
                    interactions["conversation_id"] = profile["converstion_id"]
            return {
                    "user": {
                        "user_id": profile["user_id"],
                        "username": profile["username"],
                        "first_name": profile["first_name"],
                        "last_name": profile["last_name"],
                        "sexual_preference": profile["sexual_preference"],
                        "gender": profile["gender"]
                    },
                    "profile": {
                        "biography": profile["biography"],
                        "fame_rating": profile["fame_rating"],
                    },
                    "pictures": profile["profile_picture_url"],
                    "interactions": interactions,
                    "interests": profile["interests"]
                }

        except Exception as e :
            raise Exception(e)