"""Run an isolated CTFd demo. Requires the existing CTFd source on PYTHONPATH."""
import importlib.util
import os
import secrets
import tempfile
from pathlib import Path

# Keep CTFd's import-time defaults from creating a secret file in this repository.
os.environ["SECRET_KEY"] = secrets.token_hex(32)

from CTFd import create_app
from CTFd.config import TestingConfig
from CTFd.models import Pages, UserFields, db
from CTFd.utils import set_config


def build_app():
    directory = Path(tempfile.mkdtemp(prefix="comssa-registration-demo-"))

    class DemoConfig(TestingConfig):
        SECRET_KEY = secrets.token_hex(32)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{directory / 'demo.sqlite'}"
        SERVER_NAME = None
        DEBUG = False
        TEMPLATES_AUTO_RELOAD = True
        MAIL_SERVER = None
        MAILGUN_API_KEY = None
        LOG_FOLDER = str(directory / 'logs')
        UPLOAD_FOLDER = str(directory / 'uploads')

    app = create_app(DemoConfig)
    with app.app_context():
        for key, value in {
            "setup": True, "ctf_name": "LOCAL TEST · ComSSA Hackathon 2026",
            "ctf_theme": "hackathon", "user_mode": "teams", "registration_visibility": "public",
            "account_visibility": "admins", "score_visibility": "admins",
            "challenge_visibility": "admins", "verify_emails": False,
            "mail_server": None, "mailgun_api_key": None,
            "team_size": 6, "password_min_length": 12,
            "hackathon_terms_version": "LOCAL-TEST-v1",
            "hackathon_registration_opens": "2020-01-01T00:00:00+08:00",
            "hackathon_registration_closes": "2099-01-01T00:00:00+08:00",
        }.items():
            set_config(key, value)
        for name, field_type, description in [
            ("Discord username", "text", "Your username on the hackathon Discord."),
            ("School, TAFE or university", "text", "Your current educational institution."),
            ("Current student", "boolean", "I am currently enrolled as a student."),
            ("Participation terms (LOCAL-TEST-v1)", "boolean", "I agree to the local test terms. This is not a real application."),
        ]:
            db.session.add(UserFields(name=name, field_type=field_type, description=description,
                                      required=True, public=False, editable=False))
        db.session.add(Pages(title="Local test terms", route="terms", draft=False, hidden=True,
                             content="LOCAL TEST ONLY. These are synthetic terms for testing form validation, not approved participation terms.", format="markdown"))
        db.session.commit()
    path = Path(__file__).parent / "plugin" / "__init__.py"
    spec = importlib.util.spec_from_file_location("hackathon_registration", path)
    plugin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin)
    plugin.load(app)
    return app


if __name__ == "__main__":
    build_app().run(host="127.0.0.1", port=5186, debug=False, use_reloader=False)
