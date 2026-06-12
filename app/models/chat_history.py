import uuid
from datetime import datetime
from app import db

class ChatHistory(db.Model):
    __tablename__ = "chat_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    chat_uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    transcript_uuid = db.Column(
        db.String(36),
        nullable=False,
        index=True
    )

    user_uuid = db.Column(
        db.String(36),
        nullable=False,
        index=True
    )
    video_id=db.Column(
        db.String(100),
        nullable=False
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    answer = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
 default=datetime.utcnow    )

    def repr(self):
        return f"<ChatHistory {self.chat_uuid}>"