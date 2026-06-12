from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    flash
)
import markdown

from faster_whisper import WhisperModel

from app.services.downloader import download_audio
from app.routes.mistral_ai_route import summarize, generate_title
from app.ai.vector_database import create_vector_db
from app.ai.rag_chat import ask_rag

from app.models.chat_history import ChatHistory
from app.models.transcript_history import TranscriptHistory

from app.extensions import db
from app.utils.auth import current_user, login_required

import os
import uuid
import re


video_bp = Blueprint("video", __name__)

DOWNLOAD_FOLDER = "downloads"
TRANSCRIPT_FOLDER = "transcript"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)


# =====================================================
# WHISPER MODEL
# =====================================================

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


# =====================================================
# HELPERS
# =====================================================

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def transcript_path(audio_path):
    base = os.path.splitext(
        os.path.basename(audio_path)
    )[0]

    return os.path.join(
        TRANSCRIPT_FOLDER,
        f"{base}_{uuid.uuid4().hex[:6]}.txt"
    )


# =====================================================
# VIDEO PAGE
# =====================================================

@video_bp.route("/video", methods=["GET", "POST"])
def video():

    if request.method == "POST":

        video_url = request.form.get("video_url")

        if not video_url:
            flash("Please enter a video URL", "error")
            return redirect("/video")

        return redirect(
            url_for(
                "video.process",
                url=video_url
            )
        )

    return render_template("video.html")


# =====================================================
# PROCESS VIDEO
# =====================================================

@video_bp.route("/process")
@login_required
def process():

    user = current_user()

    if not user:
        flash("Please login first", "error")
        return redirect("/login")

    video_url = request.args.get("url")

    if not video_url:
        flash("Video URL not provided", "error")
        return redirect("/video")

    try:

        video_id = str(uuid.uuid4())[:8]

        audio_path = download_audio(
            video_url,
            DOWNLOAD_FOLDER
        )

        segments, _ = model.transcribe(
            audio_path,
            task="transcribe",
            beam_size=5,
            vad_filter=True
        )


        transcript = clean_text(
            " ".join(
                segment.text
                for segment in segments
            )
        )

        if not transcript:
            flash("Transcript is empty", "error")
            return redirect("/video")

        file_path = transcript_path(audio_path)

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(transcript)

        create_vector_db(
            file_path,
            video_id
        )

        summary = summarize(transcript)
        title = generate_title(transcript)
        # summary = markdown.markdown(summary)

        transcript_record = TranscriptHistory(
            user_uuid=user.uuid,
            video_id=video_id,
            title=title,
            transcript=summary
        )

        db.session.add(transcript_record)
        db.session.commit()

        flash(
            "Video processed successfully",
            "success"
        )

        return redirect(
            url_for("video.history")
        )

    except Exception as error:

        db.session.rollback()

        print(
            "VIDEO PROCESS ERROR:",
            error
        )

        flash(
            "Failed to process video",
            "error"
        )

        return redirect("/video")


# =====================================================
# HISTORY PAGE
# =====================================================

@video_bp.route("/history")
@login_required
def history():

    user = current_user()

    if not user:
        return redirect("/login")

    transcripts = (
        TranscriptHistory.query
        .filter_by(user_uuid=user.uuid)
        .order_by(
            TranscriptHistory.created_at.desc()
        )
        .all()
    )

    return render_template(
        "history.html",
        transcripts=transcripts
    )


# =====================================================
# VIEW CHAT HISTORY
# =====================================================

@video_bp.route(
    "/history/view/<transcript_uuid>"
)
@login_required
def view_transcript_chat(
    transcript_uuid
):

    chats = (
        ChatHistory.query
        .filter_by(
            transcript_uuid=transcript_uuid
        )
        .all()
    )

    return jsonify({
        "success": True,
        "chats": [
            {
                "question": chat.question,
                "answer": chat.answer
            }
            for chat in chats
        ]
    })


# =====================================================
# CHAT API
# =====================================================

@video_bp.route(
    "/history/chat",
    methods=["POST"]
)
@login_required
def history_chat():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No JSON data received"
        }), 400

    transcript_uuid = data.get(
        "transcript_uuid"
    )

    question = data.get(
        "question"
    )

    if not transcript_uuid:
        return jsonify({
            "success": False,
            "error": "Transcript UUID missing"
        }), 400

    if not question:
        return jsonify({
            "success": False,
            "error": "Question missing"
        }), 400

    transcript = (
        TranscriptHistory.query
        .filter_by(
            transcript_uuid=transcript_uuid
        )
        .first()
    )

    if not transcript:
        return jsonify({
            "success": False,
            "error": "Transcript not found"
        }), 404

    try:

        answer, context = ask_rag(
            question,
            transcript.video_id
        )

        chat = ChatHistory(
            transcript_uuid=transcript.transcript_uuid,
            user_uuid=transcript.user_uuid,
            video_id=transcript.video_id,
            question=question,
            answer=answer
        )

        db.session.add(chat)
        db.session.commit()

        return jsonify({
            "success": True,
            "answer": answer
        })

    except Exception as error:

        db.session.rollback()

        print(
            "CHAT ERROR:",
            error
        )

        return jsonify({
            "success": False,
            "error": "Failed to generate answer"
        }), 500