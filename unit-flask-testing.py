from contextlib import contextmanager


@contextmanager
def transaction_context(test_case):
    session = test_case.app.db.session
    try:
        session.begin_nested()
        yield session
    finally:
        session.rollback()
        session.close()


import unittest
from contextlib import contextmanager
from app import app, db


@contextmanager
def transaction_context(test_case):
    session = test_case.app.db.session
    try:
        session.begin_nested()
        yield session
    finally:
        session.rollback()
        session.close()


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.db = db
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.testing = True
        self.test_app = self.app.test_client()
        self._savepoint_context = transaction_context(self)
        self._savepoint_context.__enter__()

    def tearDown(self):
        self._savepoint_context.__exit__(None, None, None)
        self.app_context.pop()
        self.app_context = None
        self.test_app = None
        self.app = None


class TestUserFeatures(TestCase):
    def test_is_slots_full(self):
        url1 = '/user=/is_slots_full'
        url2 = '/user=1/is_slots_full'

        userSlots = self.app.get(url1)

        print(userSlots)

