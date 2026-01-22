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

from geopy.geocoders import Nominatim
import ipaddress



class ProfileService:
    @staticmethod
    def create_profile(user_id: int, gender: str, sexual_preference: str,\
                        biography: str, location_set_by_user: bool, files_list, tags: str, latitude: float = 0, longitude: float = 0, ip: str = "") :
        
        # tags_list = set(tags.split(';'))
        tags_list = {tag.strip() for tag in tags.split(';') if tag.strip()}
        if ProfileRepository.find_profile_exists(user_id) :
            raise ValueError("Profile already filled!")        
        if not files_list or len(files_list) > 5 or len(files_list) < 1:
            raise ValueError("Must provide 1-5 pictures")
        TagsService.check_tag_name_valid(tags_list)
        conn = None
        injected_cursor = None
        try :
            conn = Config.DB_instence.get_connection() 
            injected_cursor = conn.cursor()

            TagsService.insert_tags(tags_list, user_id, injected_cursor)
            # print("alo", flush=True)
            PictureService.proccess_images(files_list, user_id, injected_cursor)

            if not location_set_by_user or (not latitude and not longitude) or \
                not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                result = ProfileService.initial_location(ip)
                latitude = result["lat"]
                longitude = result["lng"]
            was_done = ProfileRepository.upsert_profile(
                Profile(user_id, gender, sexual_preference, biography, location_set_by_user), injected_cursor
            )
            UserRepository.update_location(user_id, latitude, longitude, injected_cursor)
            conn.commit()
            AuthService.update_profile_profile_completion(user_id)
        except Exception as e:
            conn.rollback()
            raise
        finally:
            if injected_cursor:
                injected_cursor.close()
            if conn:
                Config.DB_instence.pool.putconn(conn)
        return was_done

    @staticmethod
    def update_location(user_id, latitude, longitude):
        try:
            result = ProfileRepository.update_location_status(user_id)
            if not result :
                raise ValueError("couldn't update your location, please try again.")
            return UserRepository.update_location(user_id, latitude, longitude)
        except ValueError:
            return False



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
            return result

        except AddressNotFoundError:
            print(f"Address {ip} not found in the database.",flush=True)
        except Exception as e:
            print(f"An error occurred: {e}", flush=True)

        return None
    
    @staticmethod
    def update_profile(user_id: int, gender: str, sexual_preference: str,\
                        biography: str, location_set_by_user: bool, files_list, tags: str, latitude: float = 0, longitude: float = 0, ip: str = "") :
        tags_list = {tag.strip() for tag in tags.split(';') if tag.strip()}    
        if files_list and len(files_list) > 5 :
            raise ValueError("Should provide 1-5 pictures")
        TagsService.check_tag_name_valid(tags_list)

        conn = None
        injected_cursor = None
        result_picures = None
        try :
            conn = Config.DB_instence.get_connection() 
            injected_cursor = conn.cursor()

            TagsService.update_tags(tags_list, user_id, injected_cursor)
            if files_list and len(files_list) > 0:
                result_picures = PictureService.update_images(files_list, user_id, injected_cursor)
            print("pictures no please", flush=True)
            if not location_set_by_user or (not latitude and not longitude) or \
                not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                result = ProfileService.initial_location(ip)
                latitude = result["lat"]
                longitude = result["lng"]
            was_done = ProfileRepository.upsert_profile(
                Profile(user_id, gender, sexual_preference, biography, location_set_by_user), injected_cursor
            )

            UserRepository.update_location(user_id, latitude, longitude, injected_cursor)
            conn.commit()
        except Exception as e:
            conn.rollback()
            if result_picures and result_picures['profile'] :
                print(f"TO DO DELETE {result_picures['url']}", flush=True)
            raise
        finally:
            if injected_cursor:
                injected_cursor.close()
            if conn:
                Config.DB_instence.pool.putconn(conn)
        return was_done
    
    @staticmethod
    def remove_picture(user_id, filename) :
        picture = PictureService.find_by_url_nd_user_id(filename, user_id)
        print (picture, flush=True)
        if picture and not picture.is_profile_picture:
            return PictureService.remove_path(picture.id, picture.url)
        return None

    @staticmethod
    def check_profile_filled(user_id: int) :
        return ProfileRepository.find_profile_exists(user_id)
    
    @staticmethod
    def get_user_address(latitude: float, longitude: float) :
        city = "Tiznit"
        country = "Morroco"
        try :

            geolocator = Nominatim(user_agent="geo_app")
            location = geolocator.reverse(f"{latitude}, {longitude}", language="en")
            address = location.raw.get('address', {})
            city = address.get('city', address.get('town', address.get('village', 'Unknown')))
            country = address.get('country', 'Unknown')
        except Exception as e:
            print(e, flush=True)
        return city, country

    @staticmethod
    def get_profile(searcher_id: int, to_find_user_id: int) :
        try :
            same = False
            if to_find_user_id== searcher_id :
                same = True

            profile = ProfileRepository.get_user_profile(user_id=to_find_user_id, my_acount=searcher_id, same=same)

            if profile is None : 
                raise ValueError("No such a profile")
            
            Address = "Not Shared!"

            if profile["location_set_by_user"] :
                city, country = ProfileService.get_user_address(profile["latitude"], profile["longitude"])
            else :
                Address = "Not Shared!"

            if same :
                interactions = {
                    "is_same": True,
                    "likes_count": profile["likes_count"],
                    "views_count": profile["views_count"]
                }
            else :
                print(profile["user_block_status"], flush=True)
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
                    interactions["conversation_id"] = profile["converstion_id"]
            return {
                    "user": {
                        "user_id": profile["user_id"],
                        "username": profile["username"],
                        "first_name": profile["first_name"],
                        "last_name": profile["last_name"],
                        "email": profile["email"] if same else None,
                        "sexual_preference": profile["sexual_preference"],
                        "gender": profile["gender"],
                        "location": Address if not profile["location_set_by_user"] else f"{city}, {country}",
                        'birthdate': profile["birthdate"] if same else ''
                    },
                    "profile": {
                        "biography": profile["biography"],
                        "fame_rating": round(min(5, max(0, (profile["fame_rating"] / 5000) * 4 + 1)), 1),
                    },
                    "pictures": profile["profile_picture_url"],
                    "interactions": interactions,
                    "interests": profile["interests"]
                }

        except Exception as e :
            raise Exception(e)

    @staticmethod
    def get_user_profile_basic(to_find_user_id: int) :
        try :
            profile = ProfileRepository.get_user_profile_basic(to_find_user_id)

            if profile is None : 
                raise ValueError("No such a profile")
            return {
                "user": {
                    "user_id": profile["user_id"],
                    "username": profile["username"]
                },
                "pictures": profile["profile_picture_url"]
            }

        except Exception as e :
            raise Exception(e)
