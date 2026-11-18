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
