from flask_sqlalchemy import SQLAlchemy
<<<<<<< Updated upstream

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'app_user'

    user_id = db.Column(db.Integer,primary_key = True )
    username = db.Columb(db.String, nullable = False)
    password = db.Column(db.String, nullable =False)
    date_created = db.Column(db.String, nullable = False)

    def __init__(self,username,password,date_created) -> None:
        self.username = username
        self.password = password
        self.date_created = date_created
=======
 
db = SQLAlchemy()
 
class User(db.Model):
   __tablename__ = 'app_user'
 
   user_id = db.Column(db.Integer,primary_key = True )
   username = db.Columb(db.String, nullable = False)
   password = db.Column(db.String, nullable =False)
   date_created = db.Column(db.String, nullable = False)
 
   def __init__(self,username,password,date_created) -> None:
       self.username = username
       self.password = password
       self.date_created = date_created
>>>>>>> Stashed changes
