from typing import List
from src.models.helpers import ValidateHelperSingleton as vhs
from models import db, Scratch, AppUser

class AppUserRepository():
    """ A static wrapper class that queries and modifies data in the app_user table.
    """

    @staticmethod
    def create_user(*, 
                    username: str,
                    user_password: str,
                    return_user: bool = False) -> AppUser:
        """ Creates a user, stores in the database, and returns the AppUser 
            instance if `return_user` is `True`
        """
        new_user = AppUser(username=username,
                           user_password=user_password)

        vhs.validate_obj_is_of_type(new_user, desired_type=AppUser)
        db.session.add(new_user)
        db.session.commit()
        if return_user is True:
            return new_user

    @staticmethod
    def check_if_user_exists(user_id: int) -> bool:
        """ Returns True if the user exists in the database,
            else returns False.
        """
        vhs.validate_id_is_int_and_pos(user_id)
        target_user = db.query.filter_by(user_id=user_id).first()
        if target_user is None:
            return False
        return True

    @staticmethod
    def return_user_if_exists(self, user_id: int) -> AppUser:
        """ Returns an AppUser instance if the user exists in the database,
            else raises a ValueError.
        """
        vhs.validate_id_is_int_and_pos(user_id)
        target_user = self.db.query.filter_by(user_id=user_id).first()
        if target_user is None:
            raise ValueError(f'Could not find user with {user_id=}')
        return target_user

class ScratchRepository():
    """ A static wrapper class that queries and modifies data in the scratch table.
    """

    @staticmethod
    def create_scratch(img, # TODO IMG VALIDATION HERE
                       *,
                       caption: str,
                       author_id: int,
                       is_comment: bool = False,
                       return_scratch=False) -> Scratch:
        """ Creates a scratch, stores in the database, and returns the
            Scratch instance if `return_scratch` is `True`.
        """
        new_scratch = Scratch(caption=caption,
                              author_id=author_id,
                              is_comment=is_comment)

        vhs.validate_obj_is_of_type(new_scratch, desired_type=Scratch)
        db.session.add(new_scratch)
        db.session.commit()
        if return_scratch is True:
            return new_scratch
    
    @staticmethod
    def comment_on_scratch(img, # TODO IMG VALIDATION HERE
                           *,
                           caption: str,
                           author_id: int,
                           op_scratch_id: int,
                           return_scratch=False) -> Scratch:
        """ Creates a scratch, stores in the database, adds reference to
            original scratch in commented_by table, and returns
            Scratch instance if `return_scratch` is `True`.
        """
        new_comment = Scratch(caption=caption,
                              author_id=author_id,
                              is_comment=True)
        vhs.validate_obj_is_of_type(new_comment, desired_type=Scratch)
        # Must post scratch to get id in order to map to parent
        # NOTE; Naive fix, could retrieve latest_scratch_id++ to get new ID
        # but this works for now :)
        db.session.add(new_comment)
        db.session.commit()
        comment_scratch_id = new_comment.scratch_id
        reply_map = CommentedBy(op_scratch_id=op_scratch_id,
                                comment_scratch_id=comment_scratch_id)
        db.session.add(reply_map)
        db.session.commit()
        if return_scratch is True:
            return new_comment
    
    @staticmethod
    def get_all_scratches() -> List[Scratch]:
        """ Returns a `List` of all scratches.
        """
        all_scratches = Scratch.query.all()
        return all_scratches

    @staticmethod
    def get_scratches_by_author(author_id: int) -> List[Scratch]:
        """ Returns all scratches by an author. Assumes the author's id
            has already been validated by the app_user repository.
        """
        scratches_by_author = Scratch.query.filter_by(author_id=author_id)
        vhs.validate_not_none(scratches_by_author)
        return scratches_by_author

ScratchRepositorySingleton = ScratchRepository()
AppUserRepositorySingleton = AppUserRepository()