"""Exercise the existing CTFd routes with synthetic accounts and an isolated SQLite DB."""
from unittest import TestCase, main
from preview import build_app
from CTFd.cache import cache
from CTFd.models import Users, Teams, UserFields, UserFieldEntries
from CTFd.utils import set_config


class RegistrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = build_app()

    def setUp(self):
        self.client = self.app.test_client()
        with self.app.app_context():
            cache.clear()
            set_config('hackathon_native_registration', False)
            set_config('registration_visibility', 'public')
            set_config('hackathon_registration_closes', '2099-01-01T00:00:00+08:00')

    def test_legacy_mode_uses_native_registration_switch(self):
        with self.app.app_context():
            set_config('hackathon_native_registration', True)
            set_config('hackathon_registration_closes', None)
        self.assertEqual(self.client.get('/register').status_code, 200)
        with self.app.app_context():
            set_config('registration_visibility', 'private')
        self.assertNotEqual(self.client.get('/register').status_code, 200)

    def payload(self, name):
        self.client.get('/register')
        with self.client.session_transaction() as session:
            data = dict(name=name, email=f'{name}@example.org', password='local-test-password-123',
                        nonce=session['nonce'], hackathon_terms_version='LOCAL-TEST-v1')
        with self.app.app_context():
            for field in UserFields.query.all():
                data[f'fields[{field.id}]'] = 'y' if field.field_type == 'boolean' else 'Test Student'
        return data

    def test_missing_terms_is_rejected(self):
        data = self.payload('missingterms')
        with self.app.app_context():
            field = UserFields.query.filter_by(name='Participation terms (LOCAL-TEST-v1)').one()
            del data[f'fields[{field.id}]']
        self.assertEqual(self.client.post('/register', data=data).status_code, 400)
        with self.app.app_context():
            self.assertIsNone(Users.query.filter_by(name='missingterms').first())

    def test_changed_terms_are_rejected(self):
        data = self.payload('oldterms')
        data['hackathon_terms_version'] = 'stale-version'
        self.assertEqual(self.client.post('/register', data=data).status_code, 400)

    def test_closed_window_rejects_direct_post(self):
        data = self.payload('lateapplicant')
        with self.app.app_context():
            set_config('hackathon_registration_closes', '2020-01-02T00:00:00+08:00')
        self.assertEqual(self.client.post('/register', data=data).status_code, 403)
        with self.app.app_context():
            self.assertIsNone(Users.query.filter_by(name='lateapplicant').first())

    def test_required_fields_and_email_validation(self):
        data = self.payload('invaliduser')
        data['email'] = 'invalid-email'
        response = self.client.post('/register', data=data)
        self.assertIn(b'valid email', response.data)
        self.assertNotIn(b'value="local-test-password-123"', response.data)
        with self.app.app_context():
            self.assertIsNone(Users.query.filter_by(name='invaliduser').first())
        data = self.payload('missingfield')
        with self.app.app_context():
            field = UserFields.query.filter_by(name='Discord username').one()
            del data[f'fields[{field.id}]']
        self.assertIn(b'required fields', self.client.post('/register', data=data).data)

    def test_native_account_team_and_duplicate_flow(self):
        data = self.payload('teamcaptain')
        self.assertEqual(self.client.post('/register', data=data).status_code, 302)
        with self.app.app_context():
            user = Users.query.filter_by(name='teamcaptain').one()
            self.assertEqual(UserFieldEntries.query.filter_by(user_id=user.id).count(), 4)
            self.assertNotEqual(user.password, data['password'])
            self.assertTrue(user.hidden)
            user_id = user.id
        self.client.get('/teams/new')
        with self.client.session_transaction() as session:
            nonce = session['nonce']
        response = self.client.post('/teams/new', data=dict(name='Local Test Team', password='team-test-password', nonce=nonce))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/welcome')
        self.assertEqual(self.client.get('/welcome').status_code, 200)
        self.client = self.app.test_client()
        duplicate = self.payload('duplicatecaptain')
        duplicate['email'] = 'TEAMCAPTAIN@example.org'
        self.assertIn(b'email has already been used', self.client.post('/register', data=duplicate).data)
        with self.app.app_context():
            self.assertEqual(Users.query.filter_by(email='teamcaptain@example.org').count(), 1)
        self.client = self.app.test_client()
        self.assertEqual(self.client.post('/register', data=self.payload('teammate')).status_code, 302)
        with self.client.session_transaction() as session:
            nonce = session['nonce']
        self.assertEqual(self.client.post('/teams/join', data=dict(name='Local Test Team', password='team-test-password', nonce=nonce)).status_code, 302)
        with self.app.app_context():
            team = Teams.query.filter_by(name='Local Test Team').one()
            self.assertEqual(Users.query.filter_by(team_id=team.id).count(), 2)
            self.assertTrue(team.hidden)
            team_id = team.id
        visitor = self.app.test_client()
        self.assertEqual(visitor.get(f'/users/{user_id}').status_code, 404)
        self.assertEqual(visitor.get(f'/teams/{team_id}').status_code, 404)

    def test_login_uses_welcome_instead_of_challenges(self):
        self.client.post('/register', data=self.payload('returninguser'))
        self.client = self.app.test_client()
        self.client.get('/login')
        with self.client.session_transaction() as session:
            nonce = session['nonce']
        response = self.client.post('/login', data=dict(name='returninguser', password='local-test-password-123', nonce=nonce))
        self.assertEqual(response.headers['Location'], '/welcome')

    def test_admin_access_is_restricted(self):
        response = self.client.get('/admin/users')
        self.assertIn(response.status_code, (302, 403))
        self.assertNotIn(b'teamcaptain@example.org', response.data)

    def test_csrf_is_enforced(self):
        data = self.payload('csrfcheck')
        data['nonce'] = 'wrong-nonce'
        self.assertEqual(self.client.post('/register', data=data).status_code, 403)


if __name__ == '__main__':
    main(verbosity=2)
