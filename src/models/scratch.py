from datetime import datetime
from random import Random

MAX_NUM_POSTS = 999_999

class Scratch():
    def __init__(self, author: str, caption: str) -> None:
        """ Initializes a Scratch object
        """
        self.author: str = author
        self.caption: str = caption
        self.date_scratched = self.format_date(datetime.now())
        self.likes: list[Scratch] = []
        self.comments: list[Scratch] = []
        self.id: int = self.create_id()
        self.href: str = self.create_href()

    def create_id(self) -> int:
        return Random().randint(0, MAX_NUM_POSTS)

    def create_href(self) -> str:
        pass

    def like_scratch(self, like_author) -> None:
        if like_author in self.likes:
            print(f'{like_author} tried to like a scratch by {self.author}, but was already liked!')
            return
        
        self.likes.append(like_author)

    def unlike_scratch(self, target_id) -> None:
        target_scratch = self.search_scratch(target_id, self.likes)
        for like_author in self.likes:
            if like_author == target_id:
                self.likes.remove(target_id)
                return

        raise NameError(f'Scratch with id {target_id} was not found in the likes of a scratch made by {self.author}')
        
    def add_comment(self, comment_scratch) -> None:
        if comment_scratch is None:
            raise TypeError(f'{comment_scratch} is none')
        if type(comment_scratch) is not Scratch:
            raise TypeError(f'{comment_scratch} is not of type Scratch')
        self.comments.append(comment_scratch)

    def search_scratch(self, target_id: int, scratch_attr):
        if target_id < 0 or target_id > MAX_NUM_POSTS:
            raise ValueError(f'{target_id} is out of range for the number of posts')
        if scratch_attr not in dir(Scratch):
            raise LookupError(f'{scratch_attr} is not an attribute of type Scratch')
        
        for scratch in scratch_attr:
            if scratch.id == target_id:
                return scratch
        return None


    @staticmethod
    def format_date(now: datetime) -> str:
        """ Returns a string for time in HH:MM AM/PM MM DD, YYYY format
        """
        hour, minute = now.time().hour, now.time().minute
        if hour > 12:
            am_or_pm = 'PM'
            hour = hour - 12
        else:
            am_or_pm = 'AM'
        month, day, year = now.month, now.day, now.year

        return f'{hour}:{minute} {am_or_pm} {month} {day}, {year}'
    
    