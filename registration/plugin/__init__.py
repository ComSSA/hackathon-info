"""Small registration guard for the existing CTFd auth.register flow."""

from datetime import datetime, timezone

from flask import has_request_context, render_template, request, url_for
from sqlalchemy import event

from CTFd.models import Pages, UserFields, Users, Teams
from CTFd.utils.decorators import authed_only
from CTFd.utils import get_config
from CTFd.utils.user import authed


def window_open(opens, closes, now=None):
    """Require explicit timezone-aware cutoffs; unconfigured registration stays closed."""
    try:
        start = datetime.fromisoformat(str(opens))
        end = datetime.fromisoformat(str(closes))
        if start.utcoffset() is None or end.utcoffset() is None:
            return False
        return start <= (now or datetime.now(timezone.utc)) < end
    except (ValueError, TypeError):
        return False


def hide_new_applicant(mapper, connection, target):
    if has_request_context() and request.endpoint in ("auth.register", "teams.new"):
        target.hidden = True


def load(app):
    # Apply privacy before insertion, avoiding any public interval after signup.
    for model in (Users, Teams):
        if not event.contains(model, "before_insert", hide_new_applicant):
            event.listen(model, "before_insert", hide_new_applicant)

    @app.route("/welcome")
    @authed_only
    def hackathon_welcome():
        return render_template(
            "page.html",
            content='<h1>Your hackathon account is ready</h1>'
            '<p>Creating an account or joining a team does not guarantee a place. '
            'Organisers review expressions of interest separately.</p>'
            '<p><a href="/team">Create or join your team</a>. '
            'Applying solo? You can find teammates through the hackathon Discord.</p>',
        )

    @app.after_request
    def registration_only_redirect(response):
        if request.endpoint in ("auth.register", "auth.login", "auth.confirm", "teams.new", "teams.join"):
            if response.status_code in (302, 303) and response.headers.get("Location") == url_for("challenges.listing"):
                response.headers["Location"] = url_for("hackathon_welcome")
        return response

    @app.before_request
    def guard_hackathon_registration():
        if request.endpoint != "auth.register" or authed():
            return None

        # Legacy registration uses CTFd's own public/private switch. The old
        # theme only required participation terms when organisers configured them.
        if get_config("hackathon_native_registration"):
            return None

        terms_version = get_config("hackathon_terms_version")
        terms = Pages.query.filter_by(route="terms", draft=False).first()
        consent = UserFields.query.filter_by(
            name=f"Participation terms ({terms_version})", field_type="boolean",
            required=True, public=False, editable=False,
        ).first()
        if not window_open(
            get_config("hackathon_registration_opens"),
            get_config("hackathon_registration_closes"),
        ) or not terms_version or not terms or not terms.content or terms.auth_required or not consent:
            return render_template(
                "page.html",
                content="<h1>Expressions of interest are closed</h1>"
                "<p>Check the hackathon website or Discord for registration announcements.</p>",
            ), 403

        if request.method == "POST" and (
            not request.form.get(f"fields[{consent.id}]")
            or request.form.get("hackathon_terms_version") != str(terms_version)
        ):
            return render_template(
                "register.html",
                errors=["Please read and accept the current participation terms before registering."],
                name=request.form.get("name", ""),
                email=request.form.get("email", ""),
            ), 400
