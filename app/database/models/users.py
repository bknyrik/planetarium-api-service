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
    users = db.relationship(
        "UserModel",
        cascade="all, delete-orphan",
        back_populates="group"
    )

    def __str__(self) -> str:
        return self.name


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False
    )
    group_id = db.Column(
        db.Integer,
        db.ForeignKey("user_groups.id", ondelete="CASCADE"),
        nullable=False
    )
    group = db.relationship(UserGroupModel, back_populates="users")
    reservations = db.relationship(
        "planetarium.ReservationModel",
        cascade="all, delete-orphan",
        back_populates="user"
    )

    def __str__(self) -> str:
        return self.email
