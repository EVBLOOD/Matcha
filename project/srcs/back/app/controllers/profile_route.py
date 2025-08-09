from flask import Blueprint, request, jsonify
from app.services.profile_service import ProfileService
# from app.services.picture_service import PictureService
from app.core.security import Security
from PIL import Image


profile_bp = Blueprint('profile_api', __name__, url_prefix='/profile')


@profile_bp.route('/create_profile', methods=['POST'])
@Security.auth_guard(check_profile=False)
def create_profile() :
    try :

        user_id = request.user_id
        body = request.form
        files = request.files

        if not files or not body or not all(key in body for key in ['gender', 'sexual_preference', 'biography', 'location_set_by_user', 'latitude', 'longitude']):
            raise ValueError("Missing required fields")

        was_added = ProfileService.create_profile(user_id=user_id, gender=body['gender'],\
                                                   sexual_preference=body['sexual_preference'], \
                                                    biography=body['biography'], \
                                                        location_set_by_user=body['location_set_by_user'], \
                                                            latitude=body['latitude'], longitude=body['longitude'], files_list=files)
        print (was_added)
        if was_added :
            return jsonify({"success": "profile created for user"}), 201
        else :
            return jsonify({"error": "server error"}), 500
    except ValueError as e :
        return jsonify({"error": str(e)}), 400


# @profile_bp.route('/update_profile', methods=['POST'])
# @Security.auth_guard()
# def update_profile() :
#     try :
#         body = request.get_json()
#         user_id = request.user_id
#         if not body or not all(key in body for key in ['gender', 'sexual_preference', 'biography', 'location_set_by_user', 'latitude', 'longitude']):
#             return jsonify({"error": "Missing required fields"}), 400
#         # if 'file' not in request.files:
#         #     return jsonify({'error': 'No file part'}), 400
#         # if file.filename == '':
#         #     return jsonify({'error': 'No selected file'}), 400
#     # import uuid
# # filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
# # try:
# #     Image.open(file.stream).verify()  # Verify without loading into memory
# #     file.stream.seek(0)  # Reset file pointer after verification
# # except:
# #     return jsonify({'error': 'Invalid image file'}), 400
#         was_added = ProfileService.update_profile(user_id=user_id, gender=body['gender'],\
#                                                    sexual_preference=body['sexual_preference'], \
#                                                     biography=body['biography'], \
#                                                         location_set_by_user=body['location_set_by_user'], \
#                                                             latitude=body['latitude'], longitude=body['longitude'])
#         if was_added :
#             return jsonify({"profile created for user"}), 201
#         else :
#             return jsonify({"server error"}), 500
#     except ValueError as e :
#         return jsonify({"error": str(e)}), 400

# # from flask import send_from_directory

# # @app.route('/uploads/<filename>')
# # def uploaded_file(filename):
# #     return send_from_directory(UPLOAD_FOLDER, filename)

