from enum import StrEnum, auto

from app.extensions import db


class UserGroupEnum(StrEnum):
    USER = auto()
    MODERATOR = auto()
    ADMIN = auto()


class UserGroupModel(db.Model):
    __tablename__ = "user_groups"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Enum(UserGroupEnum), unique=True, nullable=False)

    def __str__(self) -> str:
        return self.name
