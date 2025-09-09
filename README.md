# super-duper-octo-succotash

Simple Flask-based web email client and storage for the `chargepath.co` domain.

## Features
- Compose and send email using configurable SMTP settings
- Store sent messages in a local SQLite database
- Minimal web UI for viewing inbox and composing messages

## Running the app
```bash
pip install -r requirements.txt
python app.py
```
The application creates an `emails.db` SQLite database in the project directory.

To enable SMTP sending, set the following environment variables before running:
```bash
export SMTP_SERVER=smtp.chargepath.co
export SMTP_PORT=587  # optional, defaults to 587
export SMTP_USER=your_username  # optional
export SMTP_PASS=your_password  # optional
export SMTP_TLS=1               # optional, defaults to 1
```
Without `SMTP_SERVER`, messages are only stored locally.

## Tests
Run `pytest` to execute the unit tests.
