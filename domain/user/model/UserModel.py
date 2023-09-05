from utils.db.v2.DBUtils import Base
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Boolean

class UserModel(Base):
    __tablename__ = 'user'

    cid = Column("cid", BigInteger, primary_key=True, autoincrement=True)
    id = Column("id", String(36), unique=True, nullable=False)
    login_type = Column("login_type", String(10), nullable=False)
    social_platform = Column("social_platform", String(10), nullable=True)
    social_platform_id = Column("social_platform_id", String(100), nullable=True)
    username = Column("username", String(50), nullable=True)
    password = Column("password", String(255), nullable=True)
    salt = Column("salt", String(36), nullable=True)
    email = Column("email", String(50), nullable=True)
    name = Column("name", String(15), nullable=True)
    nickname = Column("nickname", String(20), nullable=True)
    phone_number = Column("phone_number", String(12), nullable=True)
    roles = Column("roles", String(50), nullable=False)
    profile_image_uri = Column("profile_image_uri", String(300), nullable=True)
    allowed_access_count = Column("allowed_access_count", Integer, nullable=False)
    updated_at = Column("updated_at", DateTime(timezone = True), nullable=True)
    created_at = Column("created_at", DateTime(timezone = True), nullable=True)
    deleted_flag = Column("deleted_flag", Boolean, nullable=False)

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
    def to_model(dto):
        model = UserModel()
        model.id = dto.id
        model.login_type = dto.login_type
        model.social_platform = dto.social_platform
        model.social_platform_id = dto.social_platform_id
        model.username = dto.username
        model.password = dto.password
        model.salt = dto.salt
        model.email = dto.email
        model.name = dto.name
        model.nickname = dto.nickname
        model.phone_number = dto.phone_number
        model.roles = dto.roles
        model.profile_image_uri = dto.profile_image_uri
        model.allowed_access_count = dto.allowed_access_count
        model.updated_at = dto.updated_at
        model.created_at = dto.created_at
        model.deleted_flag = dto.deleted_flag
        return model
