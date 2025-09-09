import os
import sys
import tempfile

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, Email


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
    yield app.test_client()
    os.close(db_fd)
    os.unlink(db_path)


def test_email_storage(client):
    data = {
        "sender": "tester@chargepath.co",
        "recipient": "user@example.com",
        "subject": "Test subject",
        "body": "Hello from tests",
    }
    response = client.post("/send", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test subject" in response.data
    with app.app_context():
        saved = Email.query.first()
        assert saved.sender == data["sender"]
        assert saved.recipient == data["recipient"]
