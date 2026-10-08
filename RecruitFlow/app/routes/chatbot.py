from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    flash,
    make_response
)

from reportlab.pdfgen import canvas
import io

from app.database.db import db
from app.models.chatbot_history import ChatbotHistory
from app.services.chatbot_service import ChatbotService


chatbot_bp = Blueprint(
    "chatbot",
    __name__
)


# --------------------------------------------------
# Open Chatbot
# --------------------------------------------------

@chatbot_bp.route("/chatbot/<int:candidate_id>")
def chatbot(candidate_id):

    # Allow Admin or Candidate
    if "candidate_id" not in session and "user_id" not in session:
        return redirect(url_for("candidate_auth.login"))

    if "candidate_id" in session and session["candidate_id"] != candidate_id:
        return redirect(url_for("candidate_auth.login"))

    chats = ChatbotHistory.query.filter_by(
        candidate_id=candidate_id
    ).all()

    return render_template(
        "chatbot.html",
        candidate_id=candidate_id,
        chats=chats
    )

# --------------------------------------------------
# Send Question
# --------------------------------------------------

@chatbot_bp.route(
    "/chatbot/send",
    methods=["POST"]
)
def send():

    data = request.get_json()

    candidate_id = data.get("candidate_id")

    question = data.get("question")

    if "user_id" not in session:
        if "candidate_id" not in session or session["candidate_id"] != candidate_id:
            return jsonify(
                {
                    "error": "Unauthorized"
                }
            ), 401

    if not question:

        return jsonify(
            {
                "error": "Question Required"
            }
        )

    try:

        chat = ChatbotService.ask(
            candidate_id,
            question
        )

        return jsonify({

            "question": chat.user_question,

            "answer": chat.ai_answer

        })

    except Exception as e:

        return jsonify(
            {
                "error": str(e)
            }
        )


# --------------------------------------------------
# Download Chat PDF
# --------------------------------------------------

@chatbot_bp.route(
    "/chatbot/pdf/<int:candidate_id>"
)
def pdf(candidate_id):

    if "candidate_id" not in session and "user_id" not in session:
        return redirect(url_for("candidate_auth.login"))

    if "candidate_id" in session and session["candidate_id"] != candidate_id:
        return redirect(url_for("candidate_auth.login"))

    chats = ChatbotHistory.query.filter_by(

        candidate_id=candidate_id

    ).all()

    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle("AI Resume Chat")

    y = 800

    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        40,
        y,
        "RecruitFlow AI Resume Chat"
    )

    y -= 40

    pdf.setFont(
        "Helvetica",
        11
    )

    for chat in chats:

        pdf.drawString(
            40,
            y,
            "Question:"
        )

        y -= 18

        pdf.drawString(
            50,
            y,
            chat.user_question[:90]
        )

        y -= 25

        pdf.drawString(
            40,
            y,
            "Answer:"
        )

        y -= 20

        lines = chat.ai_answer.split("\n")

        for line in lines:

            pdf.drawString(
                50,
                y,
                line[:95]
            )

            y -= 18

            if y < 60:

                pdf.showPage()

                y = 800

        y -= 25

    pdf.save()

    buffer.seek(0)

    response = make_response(
        buffer.read()
    )

    response.headers["Content-Type"] = "application/pdf"

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=AI_Resume_Chat.pdf"

    return response


# --------------------------------------------------
# Clear Chat History
# --------------------------------------------------

@chatbot_bp.route(
    "/chatbot/clear/<int:candidate_id>"
)
def clear(candidate_id):

    if "candidate_id" not in session and "user_id" not in session:

        return redirect(
            url_for("candidate_auth.login")
        )

    if "candidate_id" in session and session["candidate_id"] != candidate_id:
        return redirect(url_for("candidate_auth.login"))

    ChatbotHistory.query.filter_by(

        candidate_id=candidate_id

    ).delete()

    db.session.commit()

    flash(
        "Chat History Cleared Successfully",
        "success"
    )

    return redirect(

        url_for(

            "chatbot.chatbot",

            candidate_id=candidate_id

        )

    )


# --------------------------------------------------
# Delete One Chat
# --------------------------------------------------

@chatbot_bp.route(
    "/chatbot/delete/<int:chat_id>"
)
def delete(chat_id):

    if "candidate_id" not in session and "user_id" not in session:

        return redirect(
            url_for("candidate_auth.login")
        )

    chat = ChatbotHistory.query.get_or_404(
        chat_id
    )

    candidate_id = chat.candidate_id

    if "candidate_id" in session and session["candidate_id"] != candidate_id:
        return redirect(url_for("candidate_auth.login"))

    db.session.delete(chat)

    db.session.commit()

    flash(
        "Chat Deleted Successfully",
        "success"
    )

    return redirect(

        url_for(

            "chatbot.chatbot",

            candidate_id=candidate_id

        )

    )