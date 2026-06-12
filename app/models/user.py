import uuid
from sqlalchemy import text
from app import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())

    
    )

    username = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    profession = db.Column(
        db.String(250),
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    purpose = db.Column(
        db.String(100),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user",
        server_default=text("'user'")
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def repr(self):
        return f"<User {self.username}>"