from app.dal.models.picture import Picture
from app.dal.repositories.pictures_repository import PicturesRepository
from typing import Optional
import re
import imghdr
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
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @classmethod
    def validate_image(cls, file_stream, filename):
        filename = secure_filename(filename)
        if not cls.allowed_file(filename):
            raise ValueError("File extension not allowed")
        
        file_stream.seek(0)
        actual_extension = imghdr.what(file_stream)
        if not actual_extension:
            raise ValueError("Not a valid image file")
        
        try:
            file_stream.seek(0)
            img = Image.open(file_stream)
            img.verify()
            if img.width > Config.max_width or img.height > Config.max_height:
                raise ValueError("Invalid image size")
            # img.close()
        except Exception as e:
            raise ValueError("Invalid image content")
        
        return True

    def save_file(file) :
        file.stream.seek(0)
        ext = imghdr.what(file.stream)
        file.stream.seek(0)
        filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)
        return filename

    @classmethod
    def proccess_images(cls, list_files, user_id) :
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
            PicturesRepository.insert_picture(tmp)
        


    # def is_malware(file_stream):
    #     file_stream.seek(0)
    #     mime = magic.from_buffer(file_stream.read(2048), mime=True)
    #     return not mime.startswith('image/')