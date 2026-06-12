import uuid
from datetime import datetime
from app import db

class TranscriptHistory(db.Model):
    __tablename__ = "transcript_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    transcript_uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    user_uuid = db.Column(
        db.String(36),
        nullable=False,
        index=True
    )

    video_id = db.Column(
        db.String(100),
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    transcript = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
 default=datetime.utcnow    )

    def repr(self):
        return f"<Transcript {self.title}>"