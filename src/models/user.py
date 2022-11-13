from scratch import Scratch

class User():
    def __init__(self, username: str):
        """ Initializes a user
        """
        self.username: str = username
        self.scratch_history: list[int] = []
        self.comment_history: list[int] = []
        self.like_history: list[int] = []

    def create_scratch(self, caption) -> None:
        scratch = Scratch(
            author=self.username,
            caption=caption
        )

        self.scratch_history.append(scratch.id)
        # TODO db functionality

    def like_scratch(self, target_id: int) -> None:
        # TODO search in db
        target_scratch = None  #
        self.like_history.append(target_scratch.id)        

    def comment_on_scratch(self, target_id: int) -> None:
        # TODO comment
        target_scratch = None
        self.comment_history.append(target_scratch)
        pass
