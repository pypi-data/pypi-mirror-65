from unittest import TestCase

from avatar_utils.rest_base import *


class UnitTest(TestCase, AbstractApp):
    app = None
    db = None

    def setUp(self):
        TestCase.setUp(self)
        try:
            print('SQLALCHEMY_DATABASE_URI: %s' % self.app.config['SQLALCHEMY_DATABASE_URI'])
        except KeyError:
            pass

        self.assertFalse(self.app is None)
        self.assertFalse(self.client is None)
        self.assertTrue(self.app.config['TESTING'])

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()
        super().setUp()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()
        TestCase.tearDown(self)


class BaseUnitTest(UnitTest):
    from app import create_app, db

    app = create_app('testing')
    client = app.test_client()
    db = db


class IntegrationTest(TestCase, RemoteApp):
    pass
