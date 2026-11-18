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

    def __str__(self) -> str:
        return self.name


class AstronomyShowModel(db.Model):
    __tablename__ = "astronomy_shows"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __str__(self) -> str:
        return self.name


class PlanetariumDomeModel(db.Model):
    __tablename__ = "planetarium_domes"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    rows = db.Column(db.Integer, nullable=False)
    seats_in_row = db.Column(db.Integer, nullable=False)

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
