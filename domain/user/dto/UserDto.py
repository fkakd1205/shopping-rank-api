from dataclasses import dataclass

@dataclass
class UserDto():
    id = None
    login_type = None
    social_platform = None
    social_platform_id = None
    username = None
    password = None
    salt = None
    email = None
    name = None
    nickname = None
    phone_number = None
    roles = None
    profile_image_uri = None
    allowed_access_count = None
    updated_at = None
    created_at = None
    deleted_flag = None
        
    @staticmethod
    def to_dto(model):
        dto = UserDto()
        dto.id = model.id
        dto.login_type = model.login_type
        dto.social_platform = model.social_platform
        dto.social_platform_id = model.social_platform_id
        dto.username = model.username
        dto.password = model.password
        dto.salt = model.salt
        dto.email = model.email
        dto.name = model.name
        dto.nickname = model.nickname
        dto.phone_number = model.phone_number
        dto.roles = model.roles
        dto.profile_image_uri = model.profile_image_uri
        dto.allowed_access_count = model.allowed_access_count
        dto.updated_at = model.updated_at
        dto.created_at = model.created_at
        dto.deleted_flag = model.deleted_flag
        return dto