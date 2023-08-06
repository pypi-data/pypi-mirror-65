from unittest import TestCase

from app import db
from .rest_base import AbstractApp, LocalApp, RemoteApp


class UnitTest(TestCase, LocalApp):
    def setUp(self):
        super().setUp()
        print('SQLALCHEMY_DATABASE_URI: %s' % self.app.config['SQLALCHEMY_DATABASE_URI'])

        self.assertFalse(self.app is None)
        self.assertFalse(self.client is None)
        self.assertTrue(self.app.config['TESTING'])

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        super().tearDown()


class WithUser(TestCase, AbstractApp):
    # credentials of default test user
    test_key = 'test'
    test_username = 'test'
    test_password = 'test'
    # actual test user id in used database
    id_test_user = None

    def login_test_user(self):
        print('Logging test user')
        self.post('/user/import',
                  dict(username=self.test_username, email='avatarservsup@gmail.com', password=self.test_password,
                       lastname=self.test_key, firstname=self.test_key, middlename=self.test_key, is_student=True,
                       is_researcher=True, scopus_id='57200213601', isu_id='140883', overwrite=False))
        res = self.login(self.test_username, self.test_password)
        print(res.json)
        return res.json["result"]["user_id"]

    def setUp(self):
        super().setUp()
        self.id_test_user = self.login_test_user()
        self.assertFalse(self.id_test_user is None)


class UnitTestWithUser(WithUser, UnitTest):
    pass


class IntegrationTest(TestCase, RemoteApp):
    pass


class IntegrationTestWithUser(WithUser, IntegrationTest):
    pass
