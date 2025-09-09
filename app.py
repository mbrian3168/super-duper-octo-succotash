from datetime import datetime
import os
import smtplib
from email.message import EmailMessage

from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///emails.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(255), nullable=False)
    recipient = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/")
def index():
    emails = Email.query.order_by(Email.timestamp.desc()).all()
    return render_template("index.html", emails=emails)


@app.route("/compose")
def compose():
    return render_template("compose.html")


@app.route("/send", methods=["POST"])
def send():
    sender = request.form.get("sender")
    recipient = request.form.get("recipient")
    subject = request.form.get("subject")
    body = request.form.get("body")

    smtp_server = os.getenv("SMTP_SERVER")
    if smtp_server:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_content(body)

        with smtplib.SMTP(smtp_server, int(os.getenv("SMTP_PORT", 587))) as server:
            if os.getenv("SMTP_TLS", "1") == "1":
                server.starttls()
            user = os.getenv("SMTP_USER")
            password = os.getenv("SMTP_PASS")
            if user and password:
                server.login(user, password)
            server.send_message(msg)

    email = Email(sender=sender, recipient=recipient, subject=subject, body=body)
    db.session.add(email)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
