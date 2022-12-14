from typing import List
from src.models.helpers import ValidateHelperSingleton as vhs
from models import Like, db, Scratch, AppUser, Comment, CommentedBy, LikedBy, UserHistory


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
    def like_or_unlike_scratch(*,
                    author_id: int,
                    scratch_id: int,
                    return_like_instance: bool = False) -> Like:
        """ Likes a scratch with `scratch id` if unliked, and unlikes if the scratch
        is already liked; then returns the instance if return_like_instance is True."""
        liked_scratch = ScratchRepository.check_if_scratch_exists(scratch_id)
        author_exists = AppUserRepository.check_if_user_exists_by_id(author_id)
        if not liked_scratch:
            raise ValueError(
                f'Scratch with id {scratch_id} could not be found to like')
        if not author_exists:
            raise ValueError(f'User with {author_id=} does not exist and therefore' +
                             f'could not like scratch with id {scratch_id}')
        
        user_already_liked_scratch = AppUserRepository.user_already_liked_scratch(scratch_id, author_id)
        like_instance = None
        if user_already_liked_scratch:
            like_instance = AppUserRepository.unlike_scratch(scratch_id, author_id)
        else:
            like_instance = AppUserRepository.like_scratch(scratch_id, author_id)
        return like_instance

    @staticmethod
    def like_scratch(author_id: int, scratch_id: int) -> Like:
        """ Likes a scratch with `scratch id` and returns the Like instance.
        """
        like_instance = Like(op_scratch_id=scratch_id, author_id=author_id)
        db.session.add(like_instance)
        db.session.commit()
        return like_instance

    @staticmethod
    def unlike_scratch(author_id: int, scratch_id: int) -> bool:
        """ Unlikes a scratch with `scratch id` and returns the Like instance.
        """
        like_instance = Like.query.filter_by(
            author_id=author_id, op_scratch_id=scratch_id).first()
        db.session.delete(like_instance)
        db.session.commit()

    @staticmethod
    def user_already_liked_scratch(author_id: int, scratch_id: int) -> bool:
        """ Returns True if the user has already liked the scratch, else returns False.
        """
        like_instance = Like.query.filter_by(
            author_id=author_id, op_scratch_id=scratch_id).first()
        if like_instance is None:
            return False
        return True
    
    @staticmethod
    def get_total_number_of_scratches(user_id: int) -> int:
        all_scratches = AppUserRepository.get_scratches_by_author(user_id)
        return len(all_scratches)

    @staticmethod
    def get_number_of_likes_on_scratch(scratch_id: int) -> int:
        num_like_entries = Like.query.filter_by(op_scratch_id=scratch_id).all()
        num_likes = len(num_like_entries)
        return num_likes

    @staticmethod
    def get_total_number_of_likes_on_scratches(user_id: int) -> int:
        all_scratches_made_by_author = AppUserRepository.get_scratches_by_author(
            user_id)
        all_scratch_ids_made_by_author = [
            scratch.scratch_id for scratch in all_scratches_made_by_author]
        scratches_liked_by_users = Like.query.filter(
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

    @staticmethod
    def get_all_scratches_and_their_authors() -> dict[Scratch, AppUser]:
        """ Returns a `List` of all scratches.
        """
        all_scratches_and_their_authors = {}
        all_scratches = Scratch.query.all()
        for scratch in all_scratches:
            author = AppUserRepository.return_user_by_id(scratch.author_id)
            all_scratches_and_their_authors[scratch] = author
        return all_scratches_and_their_authors

class CommentRepository():
    """A static wrapper class for the comment table that queries and modifies 
    comment data in the database.
    """
    @staticmethod
    def add_comment(op_scratch_id: int, comment_text: str, author_id: int) -> Comment:
        """ Adds a comment to the database and returns the comment instance.
        """
        new_comment = Comment(op_scratch_id=op_scratch_id,
                              comment_text=comment_text,
                              author_id=author_id)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment
    
    @staticmethod
    def get_comment_author_with_id(comment_id: int) -> AppUser:
        """ Returns the author of a comment given `comment_id`.
        """
        vhs.validate_id_is_int_and_pos(comment_id)
        target_comment = CommentRepository.find_comment_with_id(comment_id)
        author = AppUserRepository.return_user_by_id(target_comment.author_id)
        return author

    @staticmethod
    def get_comment_and_author_with_id(comment_id: int) -> tuple[Comment, AppUser]:
        """ Returns the comment and author of a comment given `comment_id`.
        """
        vhs.validate_id_is_int_and_pos(comment_id)
        target_comment = CommentRepository.find_comment_with_id(comment_id)
        author = AppUserRepository.return_user_by_id(target_comment.author_id)
        return target_comment, author

    @staticmethod
    def get_authors_from_comments(comments: List[Comment]) -> List[AppUser]:
        """ Returns a `List` of authors from a `List` of comments.
        """
        authors = []
        for comment in comments:
            author = AppUserRepository.return_user_by_id(comment.author_id)
            authors.append(author)
        return authors

    @staticmethod
    def get_comments_and_authors_from_id(op_scratch_id: int) -> dict[Comment, AppUser]:
        """ Returns a `Dict` of comments and their authors.
        """
        comments_and_authors = {}
        comments = CommentRepository.get_all_comments_on_scratch(op_scratch_id)
        for comment in comments:
            author = AppUserRepository.return_user_by_id(comment.author_id)
            comments_and_authors[comment] = author
        return comments_and_authors

    @staticmethod
    def get_all_comments_on_scratch(op_scratch_id: int) -> List[Comment]:
        """ Returns a `List` of all comments on a scratch given `op_scratch_id`.
        """
        vhs.validate_id_is_int_and_pos(op_scratch_id)
        all_comments_on_scratch = Comment.query.filter_by(op_scratch_id=op_scratch_id).all()
        return all_comments_on_scratch
    
    @staticmethod
    def get_number_of_comments_on_scratch(op_scratch_id: int) -> int:
        """ Returns the number of comments on a scratch given `op_scratch_id`.
        """
        vhs.validate_id_is_int_and_pos(op_scratch_id)
        all_comments_on_scratch = Comment.query.filter_by(op_scratch_id=op_scratch_id).all()
        return len(all_comments_on_scratch)


ScratchRepositorySingleton = ScratchRepository()
AppUserRepositorySingleton = AppUserRepository()
CommentRepositorySingleton = CommentRepository()