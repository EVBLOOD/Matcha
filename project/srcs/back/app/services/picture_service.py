from app.dal.models.picture import Picture
from app.dal.repositories.pictures_repository import PicturesRepository
from typing import Optional
import re
# import imghdr
from PIL import Image
from app.core.config import Config
import uuid
import os
# import magic
from werkzeug.utils  import secure_filename

class PictureService:

    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].upper() in Config.ALLOWED_EXTENSIONS

    @classmethod
    def validate_image(cls, file_stream, filename):
        filename = secure_filename(filename)
        if not cls.allowed_file(filename):
            raise ValueError("File extension not allowed")
        
        # file_stream.seek(0)
        # actual_extension = imghdr.what(file_stream)
        # if not actual_extension:
        #     raise ValueError("Not a valid image file")
        
        try:
            file_stream.seek(0)
            img = Image.open(file_stream)
            img.verify()

            file_stream.seek(0)
            img = Image.open(file_stream)

            if img.format not in Config.ALLOWED_EXTENSIONS:
                raise ValueError(f"Invalid image format: {img.format}")
            
            if img.width > Config.max_width or img.height > Config.max_height:
                raise ValueError(f"Image too large ({img.width}x{img.height})")
            # img.close()
        except Exception as e:
            print(e, flush=True)
            raise ValueError("Invalid image content")
        file_stream.seek(0)
        return True

    def save_file(file) :
        file.stream.seek(0)
        img = Image.open(file.stream)
        ext = img.format.lower() if img.format else "jpg"

        filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join("app/"+Config.UPLOAD_FOLDER, filename)
        
        file.stream.seek(0)
        file.save(file_path)
        return filename



    def remove_path(id, url) :
        print(url, flush=True)
        try :
            if PicturesRepository.delete(id) :
                file_path = os.path.join(Config.UPLOAD_FOLDER, url)
                if os.path.exists(file_path):
                    os.remove(file_path)
                return True
            return None
        except :
            return None

    @classmethod
    def proccess_images(cls, list_files, user_id, injected_cursor = None) :
        profile = False
        for file in list_files :
            if file == 'profile' :
                profile = True
            cls.validate_image(list_files[file].stream, list_files[file].filename)

        if not profile :
            raise ValueError("No profile was setted")

        for file in list_files :
            tmp = cls.save_file(list_files[file])
            tmp = Picture(id=0, user_id=user_id,url=tmp, is_profile_picture=(True if file == "profile" else False))
            PicturesRepository.insert_picture(tmp, injected_cursor)

    @classmethod
    def update_images(cls, list_files, user_id, injected_cursor = None) :
        list_tmp = []
        current_pictures = len(PictureService.find_many_by_user_id(user_id))
        if len(list_files) + current_pictures > 5:
            raise ValueError("You can't upload this much of pictures!")
        profile = False
        for file in list_files :
            if file == 'profile' :
                profile = True
            cls.validate_image(list_files[file].stream, list_files[file].filename)

        for file in list_files :
            tmp_file = cls.save_file(list_files[file])
            tmp = Picture(id=0, user_id=user_id,url=tmp_file, is_profile_picture=(True if file == "profile" else False))

            if file == "profile" :
                profile_url = tmp_file
                PicturesRepository.update_picture_profile(tmp_file, user_id, injected_cursor)
                print("current_pictures", flush=True)
            else :
                PicturesRepository.insert_picture(tmp, injected_cursor)
            list_tmp.append(tmp_file)

        if profile :
            return {"profile": True, "url": profile_url, "failed": list_tmp} 

        return {"profile": False, "url": "tmp", "failed": list_tmp} 

    @classmethod
    def find_many_by_user_id(cls, user_id) :
        return PicturesRepository.find_many_by_user_id(user_id)


    @classmethod
    def find_by_url_nd_user_id(cls, url: str, user_id: str) :
        return PicturesRepository.find_by_url_nd_user_id(url, user_id)

    # def is_malware(file_stream):
    #     file_stream.seek(0)
    #     mime = magic.from_buffer(file_stream.read(2048), mime=True)
    #     return not mime.startswith('image/')