from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Scratch(db.Model):
    MAX_CAPTION_LENGTH = 40
    MAX_DATE_LENGTH = 20
    __tablename__ = 'scratch'
    scratch_id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(MAX_CAPTION_LENGTH), nullable=True)
    author_id = db.Column(db.Integer, nullable=False)
    is_comment = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.String(MAX_DATE_LENGTH), nullable=False)