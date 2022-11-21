from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy()

# BUG: CAUSING ISSUES--
# """AmbiguousForeignKeysError: Could not determine join condition between parent/child tables on relationship Scratch._ - there are multiple foreign key paths linking the tables via secondary table 'commented_by'. Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference from the secondary table to each of the parent and child tables."
op_scratch_id=db.Column('op_scratch_id', db.Integer, db.ForeignKey('Scratch.scratch_id'), primary_key=True),
comment_scratch_id=db.Column('comment_scratch_id', db.Integer, db.ForeignKey('Scratch.scratch_id'), primary_key=True)
commented_by = db.Table('commented_by',
    op_scratch_id,
    comment_scratch_id
    # foreign_keys=['op_scratch_id', 'comment_scratch_id'],
)


class Scratch(db.Model):
    MAX_CAPTION_LENGTH = 40
    MAX_DATE_LENGTH = 20
    __tablename__ = 'scratch'
    scratch_id = db.Column(db.Integer, db.ForeignKey('commented_by.op_scratch_id'), primary_key=True)
    caption = db.Column(db.String(MAX_CAPTION_LENGTH), nullable=True)
    author_id = db.Column(db.Integer, nullable=False)
    is_comment = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _ = db.relationship('Scratch', secondary=commented_by, backref='op_scratch_id')
    # __ = db.relationship('Scratch', secondary=commented_by, backref='comment_scratch_id')


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
    MAX_USERNAME_LENGTH = 16
    MAX_PASSWORD_LENGTH = 32 
    __tablename__ = 'app_user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(MAX_USERNAME_LENGTH), nullable=False)
    user_password = db.Column(db.String(MAX_PASSWORD_LENGTH), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, username: str, user_password: str) -> None:
        self.username = username
        self.user_password = user_password

    def repr(self) -> str:
        return f'AppUser({self.user_id=}, {self.username=}, {self.user_password=}, {self.date_created=})'


class LikedBy(db.Model):
    scratch_id = db.Column(db.Integer, db.ForeignKey('scratch.scratch_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), primary_key=True)
    scratch = db.relationship('Scratch', backref='liked_by_scratch', lazy=True)
    user = db.relationship('AppUser', backref='user_that_liked', lazy=True)
