from app.dal.models.profile import Profile
from app.dal.repositories.profile_repository import ProfileRepository
from typing import Optional
import re
import imghdr  # Built-in module for checking image types
from io import BytesIO
from PIL import Image


class ProfileService:
    @staticmethod
    def create_profile(user_id: int, gender: str, sexual_preference: str,\
                        biography: str, location_set_by_user: bool, latitude: float, longitude: float) :
        if gender not in ('male', 'female', 'other') \
            or sexual_preference not in ('straight', 'gay', 'bisexual') \
                or not isinstance(location_set_by_user, bool):
            raise ValueError("Form error inputs!")
        if ProfileRepository.find_profile_exists(user_id) :
            raise ValueError("Profile already filled!")

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
    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
@staticmethod
def validate_image(file_stream, filename):

    # Check 1: Verify the file extension is allowed
    if not allowed_file(filename):
        return False, "File extension not allowed"
    
    # Check 2: Verify the file signature matches image formats
    file_stream.seek(0)
    actual_extension = imghdr.what(file_stream)
    if not actual_extension:
        return False, "Not a valid image file"
    
    # Check 3: Verify the extension matches the actual image type
    claimed_extension = filename.rsplit('.', 1)[1].lower()
    extension_map = {
        'jpg': 'jpeg',
        'jpeg': 'jpeg',
        'png': 'png',
        'gif': 'gif'
    }
    
    if extension_map.get(claimed_extension) != actual_extension:
        return False, "File extension doesn't match actual image type"
    
    # Check 4: Verify the image can be opened by PIL (checks for corruption)
    try:
        file_stream.seek(0)
        img = Image.open(file_stream)
        img.verify()  # Verify without loading pixel data
        file_stream.seek(0)
    except Exception as e:
        return False, f"Invalid image content: {str(e)}"
    
    return True, None