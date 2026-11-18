from app.extensions import db


AstronomyShowShowThemesModel = db.Table(
    "astronomy_show_show_themes",
    db.Model.metadata,
    db.Column(
        "astronomy_show_id",
        db.ForeignKey("astronomy_shows.id"),
        primary_key=True
    ),
    db.Column(
        "show_theme_id",
        db.ForeignKey("show_themes.id"),
        primary_key=True
    )
)


class ShowThemeModel(db.Model):
    __tablename__ = "show_themes"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    astronomy_shows = db.relationship(
        "AstronomyShowModel",
        secondary=AstronomyShowShowThemesModel,
        back_populates="show_themes"
    )

    def __str__(self) -> str:
        return self.name


class AstronomyShowModel(db.Model):
    __tablename__ = "astronomy_shows"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    show_themes = db.relationship(
        ShowThemeModel,
        secondary=AstronomyShowShowThemesModel,
        back_populates="astronomy_shows"
    )
    show_sessions = db.relationship(
        "ShowSessionModel",
        cascade="all, delete-orphan",
        back_populates="astronomy_show"
    )

    def __str__(self) -> str:
        return self.name


class PlanetariumDomeModel(db.Model):
    __tablename__ = "planetarium_domes"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    rows = db.Column(db.Integer, nullable=False)
    seats_in_row = db.Column(db.Integer, nullable=False)
    show_sessions = db.relationship(
        "ShowSessionModel",
        cascade="all, delete-orphan",
        back_populates="planetarium_dome"
    )

    def __str__(self) -> str:
        return self.name


class ShowSessionModel(db.Model):
    __tablename__ = "show_sessions"

    id = db.Column(db.Integer, primary_key=True, index=True)
    astronomy_show_id = db.Column(
        db.Integer,
        db.ForeignKey("astronomy_shows.id", ondelete="CASCADE"),
        nullable=False
    )
    planetarium_dome_id = db.Column(
        db.Integer,
        db.ForeignKey("planetarium_dome.id", ondelete="CASCADE"),
        nullable=False
    )
    show_time = db.Column(db.DateTime, nullable=False)
    astronomy_show = db.relationship(
        AstronomyShowModel,
        back_populates="show_sessions"
    )
    planetarium_dome = db.relationship(
        PlanetariumDomeModel,
        back_populates="show_sessions"
    )


class ReservationModel(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        nullable=False
    )
    user = db.relationship(
        "users.UserModel",
        back_populates="reservations"
    )


class TicketModel(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True, index=True)
    row = db.Column(db.Integer, nullable=False)
    seat = db.Column(db.Integer, nullable=False)
    reservation_id = db.Column(
        db.Integer,
        db.ForeignKey("reservations.id", ondelete="CASCADE"),
        nullable=False
    )
    show_session_id = db.Column(
        db.Integer,
        db.ForeignKey("show_sessions.id", ondelete="CASCADE"),
        nullable=False
    )
    reservation = db.relationship(
        ReservationModel,
        back_populates="tickets"
    )
    show_session = db.relationship(
        ShowSessionModel,
        back_populates="tickets"
    )
