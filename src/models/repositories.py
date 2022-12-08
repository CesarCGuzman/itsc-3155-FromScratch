from typing import List
from src.models.helpers import ValidateHelperSingleton as vhs
from models import db, Scratch, AppUser, CommentedBy, LikedBy, UserHistory


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
    def update_biography(*,
                         user_id: int,
                         new_biography: str,
                         return_updated_biography: bool = False) -> None | str:
        """ Updates a user's biography. Returns the new biography if
            `return_updated_biography` is `True`
        """
        vhs.validate_id_is_int_and_pos(user_id)
        user = AppUserRepository.return_user_by_id(user_id)
        updated_biography = user.update_biography(new_biography)
        db.session.commit()
        if return_updated_biography:
            return updated_biography

    @staticmethod
    def check_if_user_exists_by_id(user_id: int) -> bool:
        """ Returns True if the user exists in the database,
            else returns False.
        """
        vhs.validate_id_is_int_and_pos(user_id)
        target_user = AppUser.query.filter_by(user_id=user_id).first()
        if target_user is None:
            return False
        return True

    @staticmethod
    def check_if_user_exists_by_username(username: str) -> bool:
        """ Returns True if the user exists in the database,
            else returns False.
        """
        vhs.validate_username_not_empty(username)
        target_user = AppUser.query.filter_by(username=username).first()
        if target_user is None:
            return False
        return True

    @staticmethod
    def return_user_by_id(user_id: int) -> AppUser:
        """ Returns an AppUser instance by `user_id` if the user exists 
            in the database, else raises a ValueError.
        """
        vhs.validate_id_is_int_and_pos(user_id)
        target_user = AppUser.query.filter_by(user_id=user_id).first()
        if target_user is None:
            raise ValueError(f'Could not find user with {user_id=}')
        return target_user

    @staticmethod
    def return_user_by_username(username: str) -> AppUser:
        """ Returns an AppUser instance by case-sensitive `username`
            if the user exists in the database, else raises a ValueError.
        """
        target_user = AppUser.query.filter_by(username=username).first()
        if target_user is None:
            raise ValueError(f'Could not find user with {username=}')
        return target_user
        
    @staticmethod
    def like_scratch(*,
                     author_id: int,
                     scratch_id: int,
                     return_liked_by_map=False) -> None | LikedBy:
        """ Likes a scratch with `scratch id`, and stores their likes in the
            `liked_by` table. 
        """
        liked_scratch = ScratchRepository.check_if_scratch_exists(scratch_id)
        author_exists = AppUserRepository.check_if_user_exists_by_id(author_id)
        if not liked_scratch:
            raise ValueError(
                f'Scratch with id {scratch_id} could not be found to like')
        if not author_exists:
            raise ValueError(f'User with {author_id=} does not exist and therefore' +
                             f'could not like scratch with id {scratch_id}')

        liked_map = LikedBy(scratch_id, author_id)
        user_liked_scratch_history = UserHistory(
            user_id=author_id,
            parent_scratch_id=scratch_id,
            user_liked=True)
        db.session.add(liked_map)
        db.session.add(user_liked_scratch_history)
        db.session.commit()
        if return_liked_by_map:
            return liked_map

    def get_total_number_of_scratches(user_id: int) -> int:
        all_scratches = AppUserRepository.get_scratches_by_author(user_id)
        return len(all_scratches)

    def get_total_number_of_likes_on_scratches(user_id: int) -> int:
        all_scratches_made_by_author = AppUserRepository.get_scratches_by_author(
            user_id)
        all_scratch_ids_made_by_author = [
            scratch.scratch_id for scratch in all_scratches_made_by_author]
        scratches_liked_by_users = LikedBy.query.filter(
            LikedBy.scratch_id.in_(all_scratch_ids_made_by_author)).all()
        return len(scratches_liked_by_users)

    @staticmethod
    def get_scratches_by_author(author_id: int) -> List[Scratch]:
        """ Returns all scratches by an author. Assumes the author's id
            has already been validated by the app_user repository.
        """
        scratches_by_author = Scratch.query.filter_by(
            author_id=author_id).all()
        vhs.validate_not_none(scratches_by_author)
        return scratches_by_author


class ScratchRepository():
    """ A static wrapper class that queries and modifies data in the scratch table.
    """

    @staticmethod
    def create_scratch(*,
                       caption: str,
                       author_id: int,
                       is_comment: bool = False,
                       return_scratch=False) -> None | Scratch:
        """ Creates a scratch, stores in the database, and returns the
            Scratch instance if `return_scratch` is `True`.
        """

        new_scratch = Scratch(caption=caption,
                              author_id=author_id,
                              is_comment=is_comment)
        print(f'\n\n\nCreating scratch in repositories.py,\n{new_scratch=}\n{new_scratch.scratch_id=}\n\n\n')
        vhs.validate_obj_is_of_type(new_scratch, desired_type=Scratch)
        db.session.add(new_scratch)
        db.session.commit()

        # Store in the user's history
        just_created_scratch = AppUserRepository.get_scratches_by_author(author_id)[-1]
        ScratchRepository.add_url_to_scratch(just_created_scratch.scratch_id)
        user_created_scratch_history = UserHistory(
            user_id=author_id,
            parent_scratch_id=just_created_scratch.scratch_id,
            user_created_op_scratch=True
        )
        db.session.add(user_created_scratch_history)
        db.session.commit()
        if return_scratch is True:
            return new_scratch

    @staticmethod
    def add_url_to_scratch(scratch_id: int,
                           return_scratch: bool = True) -> None | Scratch:
        vhs.validate_id_is_int_and_pos(scratch_id)
        target_scratch = ScratchRepository.find_scratch_with_id(scratch_id)
        filename = ScratchRepository.create_scratch_filename(target_scratch.scratch_id, target_scratch.author_id)
        target_scratch.scratch_filename = filename
        print(f'{target_scratch} had its filename updated to {filename}')
        db.session.commit()

    @staticmethod
    def create_scratch_filename(scratch_id: int,
                                user_id: int) -> str:
        """Creates the filename for a given scratch id that 
        takes the following form:

        `scratch_id00user_id00scratch.date_created`

        Args:
            scratch_id (int): id of the scratch whose filename is being created
            user_id (int): id of the user who created the scratch

        Returns:
            str: filename of the scratch
        """
        vhs.validate_id_is_int_and_pos(scratch_id)
        vhs.validate_id_is_int_and_pos(user_id)
        target_scratch = ScratchRepository.find_scratch_with_id(scratch_id)
        date_created = target_scratch.date_created
        delim = '00'
        file_extension = '.jpeg'
        stripped_date_created = str(date_created.month) + delim + str(date_created.day) + delim + str(date_created.year)

        filename: str = str(scratch_id) + delim + str(user_id) + delim + stripped_date_created + file_extension
        return filename

    @staticmethod
    def comment_on_scratch(img,  # TODO IMG VALIDATION HERE
                           *,
                           caption: str,
                           author_id: int,
                           op_scratch_id: int,
                           return_scratch=False) -> None | Scratch:
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
        user_commented_history = UserHistory(
            user_id=author_id,
            parent_scratch_id=op_scratch_id,
            user_commented=True,
            user_comment_scratch_id=comment_scratch_id
        )
        db.session.add(reply_map)
        db.session.add(user_commented_history)
        db.session.commit()
        if return_scratch is True:
            return new_comment

    @staticmethod
    def check_if_scratch_exists(scratch_id: int) -> bool:
        """ Returns `True` if a Scratch given `scratch_id` exists,
            else returns `False`.
        """
        vhs.validate_id_is_int_and_pos(scratch_id)
        target_scratch = ScratchRepository.find_scratch_with_id(scratch_id)
        if target_scratch is None:
            return False
        else:
            return True

    @staticmethod
    def find_scratch_with_id(scratch_id: int) -> Scratch:
        """ Returns a Scratch instance given a `scratch_id`. Raises
            a ValueError if the scratch cannot be found.
        """
        vhs.validate_id_is_int_and_pos(scratch_id)
        target_scratch = Scratch.query.filter_by(scratch_id=scratch_id).first()
        vhs.validate_not_none(target_scratch)
        return target_scratch

    @staticmethod
    def get_all_scratches() -> List[Scratch]:
        """ Returns a `List` of all scratches.
        """
        all_scratches = Scratch.query.all()
        return all_scratches


ScratchRepositorySingleton = ScratchRepository()
AppUserRepositorySingleton = AppUserRepository()
