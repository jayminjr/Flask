from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(88), unique=True, nullable=False)
    password = db.Column(db.String(88), nullable=False)
