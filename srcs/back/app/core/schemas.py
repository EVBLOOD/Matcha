from marshmallow import fields, validate, ValidationError, validates_schema, pre_load, validates, ValidationError
from app.core.sanitizer import sanitize_text

from app.core.config import Config

from datetime import datetime

class UserRegisterSchema(Config.ma_instence.Schema):
    def validate_date(value):
        try:
            birthdate = datetime.strptime(str(value), '%Y-%m-%d')
            if birthdate >= datetime.now():
                raise ValidationError("Birthdate must be in the past.")
        except ValueError:
            raise ValidationError("Invalid date format.")

    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    birthdate = fields.Date(required=True, validate=validate_date)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=60))
    email = fields.Email(required=True)
    @pre_load
    def sanitize_inputs(self, data, **kwargs):
        if hasattr(data, 'to_dict'):
            data = data.to_dict()
        else:
            data = dict(data)

        if 'username' in data:
            data['username'] = sanitize_text(data['username'])
        if 'first_name' in data:
            data['first_name'] = sanitize_text(data['first_name'])
        if 'last_name' in data:
            data['last_name'] = sanitize_text(data['last_name'])
        return data


class UserLoginSchema(Config.ma_instence.Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class ProfileSchema(Config.ma_instence.Schema):
    @pre_load
    def sanitize_inputs(self, data, **kwargs):
        if hasattr(data, 'to_dict'):
            data = data.to_dict()
        else:
            data = dict(data)

        if 'biography' in data:
            data['biography'] = sanitize_text(data['biography'])
        if 'tags' in data:
            tags = data['tags'].split(';')
            sanitized_tags = [sanitize_text(t.strip()) for t in tags]
            data['tags'] = ';'.join(sanitized_tags)
        return data
    gender = fields.Str(required=True, validate=validate.OneOf(['male', 'female', 'other']))
    sexual_preference = fields.Str(required=True, validate=validate.OneOf(['straight', 'gay', 'bisexual']))
    biography = fields.Str(required=True, validate=validate.Length(max=500))
    location_set_by_user = fields.Boolean(required=True)
    latitude = fields.Decimal(required=False, places=8)
    longitude = fields.Decimal(required=False, places=8)
    tags = fields.Str(required=True)

    @validates_schema
    def validate_location(self, data, **kwargs):
        if data.get('location_set_by_user'):
            if 'latitude' not in data or data.get('latitude') is None:
                raise ValidationError("Latitude is required when location_set_by_user is true.", 'latitude')
            if 'longitude' not in data or data.get('longitude') is None:
                raise ValidationError("Longitude is required when location_set_by_user is true.", 'longitude')

class UpdateProfileSchema(Config.ma_instence.Schema):
    gender = fields.Str(required=True, validate=validate.OneOf(['male', 'female', 'other']))
    sexual_preference = fields.Str(required=True, validate=validate.OneOf(['straight', 'gay', 'bisexual']))
    biography = fields.Str(required=True, validate=validate.Length(max=500))
    location_set_by_user = fields.Boolean(required=True)
    latitude = fields.Decimal(required=False, places=8)
    longitude = fields.Decimal(required=False, places=8)
    @validates_schema
    def validate_location(self, data, **kwargs):
        if data.get('location_set_by_user'):
            if 'latitude' not in data or data.get('latitude') is None:
                raise ValidationError("Latitude is required when location_set_by_user is true.", 'latitude')
            if 'longitude' not in data or data.get('longitude') is None:
                raise ValidationError("Longitude is required when location_set_by_user is true.", 'longitude')

class UserPictureSchema(Config.ma_instence.Schema):
    url = fields.Url(required=True)
    is_profile_picture = fields.Boolean(required=False)

class UserInterestsSchema(Config.ma_instence.Schema):
    tags = fields.List(fields.Int(), required=True)

class UserInteractionSchema(Config.ma_instence.Schema):
    status = fields.Str(required=True, validate=validate.OneOf(['liked', 'disliked']))

class MessageSchema(Config.ma_instence.Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1))
    @validates('content')
    def sanitize_content(self, value):
        cleaned = sanitize_text(value)
        if not cleaned:
            raise ValidationError("Message cannot be empty")
        return cleaned

class UserReportSchema(Config.ma_instence.Schema):
    reason = fields.Str(validate=validate.Length(max=500))

class UserBlockSchema(Config.ma_instence.Schema):
    blocked_id = fields.Int(required=True)

class TokenSchema(Config.ma_instence.Schema):
    token = fields.Str(required=True)


class UpdateGeneralUserSchema(Config.ma_instence.Schema):
    def validate_date(value):
        try:
            birthdate = datetime.strptime(str(value), '%Y-%m-%d')
            if birthdate >= datetime.now():
                raise ValidationError("Birthdate must be in the past.")
        except ValueError:
            raise ValidationError("Invalid date format.")

    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    birthdate = fields.Date(required=True, validate=validate_date)


class UpdateUserPasswordSchema(Config.ma_instence.Schema):
    password = fields.Str(required=True, validate=validate.Length(min=8, max=60))


class UpdateLocation(Config.ma_instence.Schema):
    latitude = fields.Decimal(required=True, places=8)
    longitude = fields.Decimal(required=True, places=8)


class SetReport(Config.ma_instence.Schema):
    @pre_load
    def sanitize_inputs(self, data, **kwargs):
        if hasattr(data, 'to_dict'):
            data = data.to_dict()
        else:
            data = dict(data)

        if 'reason' in data:
            data['reason'] = sanitize_text(data['reason'])
        return data
    reason = fields.Str(required=True, validate=validate.Length(max=500))
    reported_id = fields.Int(required=True)