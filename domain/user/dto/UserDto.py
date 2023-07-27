class UserDto():
    def __init__(self):
        self.id = None
        self.login_type = None
        self.social_platform = None
        self.social_platform_id = None
        self.username = None
        self.password = None
        self.salt = None
        self.email = None
        self.name = None
        self.nickname = None
        self.phone_number = None
        self.roles = None
        self.profile_image_uri = None
        self.allowed_access_count = None
        self.updated_at = None
        self.created_at = None
        self.deleted_flag = None
        
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