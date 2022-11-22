from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy()


class Scratch(db.Model):
    MAX_CAPTION_LENGTH = 40
    MAX_DATE_LENGTH = 20
    __tablename__ = 'scratch'
    scratch_id = db.Column(db.Integer,
        db.ForeignKey('commented_by.op_scratch_id'),
        db.ForeignKey('liked_by.scratch_id'),
        primary_key=True,
        autoincrement=True
    )
    caption = db.Column(
        db.String(MAX_CAPTION_LENGTH),
        nullable=True
        )
    author_id = db.Column(
        db.Integer,
        nullable=False
    )
    is_comment = db.Column(
        db.Boolean,
        nullable=False
    )
    date_created = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    def __init__(self, *, caption: str, author_id: int, is_comment: bool) -> None:
        self.caption = caption
        self.author_id = author_id
        self.is_comment = is_comment
    
    def get_scratch_id(self) -> int:
        """ Returns the id of the Scratch instance.
        """
        return self.scratch_id

    def __repr__(self) -> str:
        return f'Scratch({self.scratch_id=}, {self.caption=}, {self.author_id=}, {self.is_comment=}, {self.date_created=})'


class AppUser(db.Model):
    __tablename__ = 'app_user'

    MAX_USERNAME_LENGTH = 16
    MAX_PASSWORD_LENGTH = 32 

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(MAX_USERNAME_LENGTH), nullable=False)
    user_password = db.Column(db.String(MAX_PASSWORD_LENGTH), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, username: str, user_password: str) -> None:
        self.username = username
        self.user_password = user_password

    def repr(self) -> str:
        return f'AppUser({self.user_id=}, {self.username=}, {self.user_password=}, {self.date_created=})'


class CommentedBy(db.Model):
    __tablename__ = 'commented_by'

    op_scratch_id = db.Column(
        db.Integer,
        db.ForeignKey('scratch.scratch_id'),
        primary_key=True
    )
    comment_scratch_id = db.Column(
        db.Integer,
        db.ForeignKey('scratch.scratch_id'),
        primary_key=True
    )

    def __init__(self, op_scratch_id: int, comment_scratch_id: int):
        self.op_scratch_id = op_scratch_id
        self.comment_scratch_id = comment_scratch_id


class LikedBy(db.Model):
    __tablename__ = 'liked_by'

    scratch_id = db.Column(
        db.Integer,
        db.ForeignKey('scratch.scratch_id'),
        primary_key=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('app_user.user_id'),
        primary_key=True
    )

    def __init__(self, scratch_id: int, user_id: int):
        self.scratch_id = scratch_id
        self.user_id = user_id
        