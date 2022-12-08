from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy()


class Scratch(db.Model):
    MAX_CAPTION_LENGTH = 40
    MAX_DATE_LENGTH = 20
    MAXMIMUM_FILENAME_LENGTH: int = 30
    __tablename__ = 'scratch'

    scratch_id = db.Column(db.Integer,
                           db.ForeignKey('commented_by.op_scratch_id'),
                           db.ForeignKey('liked_by.scratch_id'),
                           primary_key=True,
                           autoincrement=True,
                           nullable=False
                           )
    scratch_filename = db.Column(
        db.String(MAXMIMUM_FILENAME_LENGTH),
        nullable=True
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

    MINIMUM_FRONTEND_USERNAME_LENGTH: int = 3
    MAXIMUM_FRONTEND_USERNAME_LENGTH: int = 16
    MINIMUM_FRONTEND_PASSWORD_LENGTH: int = 8
    MAXIMUM_FRONTEND_PASSWORD_LENGTH: int = 32
    MAXIMUM_DATABASE_PASSWORD_LENGTH: int = 255
    MAXIMUM_BIOGRAPHY_LENGTH: int = 60

    user_id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(MAXIMUM_FRONTEND_USERNAME_LENGTH),
        nullable=False
    )
    user_password = db.Column(
        db.String(MAXIMUM_DATABASE_PASSWORD_LENGTH),
        nullable=False
        ) 
    date_created = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )
    biography = db.Column(
        db.String(MAXIMUM_BIOGRAPHY_LENGTH),
        nullable=True
    )

    def __init__(self, username: str, user_password: str) -> None:
        self.username = username
        self.user_password = user_password

    def update_biography(self, new_biography: str) -> None:
        if new_biography == self.biography:
            raise ValueError('Cannot replace bio since new_biography is the \
            same as the current biography')
        
        self.biography = new_biography
        
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


class UserHistory(db.Model):
    __tablename__ = "user_history"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('scratch.scratch_id'),
        primary_key=True
    )
    parent_scratch_id = db.Column(
        db.Integer,
        db.ForeignKey('scratch.scratch_id'),
        primary_key=True
    )
    user_created_op_scratch = db.Column(
        db.Boolean,
        nullable=False
    )
    user_commented = db.Column(
        db.Boolean,
        nullable=False
    )
    user_comment_scratch_id = db.Column(
        db.Integer,
        nullable=True
    )
    user_liked = db.Column(
        db.Integer,
        nullable=True
    )

    def __init__(self,
                 *,
                 user_id: int,
                 parent_scratch_id: int,
                 user_created_op_scratch: bool = False,
                 user_commented: bool = False,
                 user_comment_scratch_id: int = None,
                 user_liked: bool = False):
        """ Constructor to enter a particular user's history of actions. \
            `user_created_op_scratch`, `user_commented`, `user_liked`, and \
            `user_comment_scratch_id` are exclusive bool flags that describe the \
            action being recorded in the user's history; only one may be True at once.

        Args:
            user_id (int): `user_id` of the user whose history is being recorded
            parent_scratch_id (int): The `scratch_id` of the scratch whose history is being recorded.
            user_created_op_scratch (bool): True if user is creating a new \
                original post scratch. Defaults to False.
            user_commented (bool): True if user is commenting on another \
                scratch. `parent_scratch_id` then refers to the original scratch \
                the user is replying to, and `user_scratch_comment_id` refers \
                to the id of the scratch reply. Defaults to False.
            user_comment_scratch_id (int, optional): `scratch_id` of the comment \
                being posted by user if and only if `user_commented` is \
                True. Defaults to None.
            user_liked (bool): True if the user liked the parent scratch. \
                Defaults to False.
        """
        self.user_id = user_id
        self.parent_scratch_id = parent_scratch_id
        self.user_created_op_scratch = user_created_op_scratch
        self.user_commented = user_commented
        self.user_comment_scratch_id = user_comment_scratch_id
        self.user_liked = user_liked

        if user_commented and user_comment_scratch_id == None:
            raise ValueError(f'Must provide user_comment_scratch_id if \
            user_commented is True, received {user_comment_scratch_id=} \
            and {user_commented}')
    
    def __repr__(self) -> str:
        if self.user_created_op_scratch:
            return f'{self.user_id} created an op scratch with id {self.parent_scratch_id}'
        elif self.user_commented:
            return f'{self.user_id} commented on op scratch with id {self.parent_scratch_id} \
                with a reply scratch with id {self.user_comment_scratch_id}'
        elif self.user_liked:
            return f'{self.user_id} liked a scratch with id {self.parent_scratch_id}'
        else:
            raise ValueError('No history flag was set!')
            
