"""Apply organiser-specified private native CTFd registration fields."""
from CTFd import create_app
from CTFd.cache import cache
from CTFd.models import db, UserFields

FIELDS = [
    ('Name', 'text', True, 'Your full name.'),
    ('Phone', 'text', True, 'A phone number organisers can contact you on.'),
    ('School', 'text', True, 'Your school, TAFE or university.'),
    ('Dietary Requirements?', 'text', True, 'List dietary requirements or write None.'),
    ('Course and Year', 'text', True, 'Your course and current year of study.'),
    ('DOB', 'text', True, 'Date of birth in DD/MM/YYYY format.'),
    ('Student ID', 'text', True, 'Your student identification number.'),
    ('Discord Username', 'text', True, 'Your Discord username.'),
    ('Joined Discord?', 'boolean', False, 'Tick if you have joined the hackathon Discord. Leave unticked for No.'),
]
ALIASES = {'School': 'School, TAFE or university', 'Discord Username': 'Discord username'}
app = create_app()
with app.app_context():
    for name, kind, required, description in FIELDS:
        field = UserFields.query.filter_by(name=name).first()
        if field is None and name in ALIASES:
            field = UserFields.query.filter_by(name=ALIASES[name]).first()
        if field is None:
            field = UserFields(name=name, field_type=kind)
            db.session.add(field)
        field.name = name
        field.field_type = kind
        field.description = description
        field.required = required
        field.public = False
        field.editable = True
    db.session.commit()
    cache.clear()
    print('Configured organiser fields; Username and Email use native account fields.')
