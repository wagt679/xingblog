import unittest

from app.models import User

class UserModelsTest(unittest.TestCase):

    def test_passwd_setter(self):
        u = User(passwd="cat")
        self.assertTrue(u.password_hash is not None)

    def test_passwd_getter(self):
        u = User(passwd="cat")
        with self.assertRaises(AttributeError):
            u.passwd

    def test_passwd_verification(self):
        u = User(passwd = "cat")
        self.assertTrue(u.verify_passwd("cat"))
        self.assertFalse(u.verify_passwd("dog"))

    def test_passed_salts_are_random(self):
        u1 = User(passwd="cat")
        u2 = User(passwd="cat")
        self.assertTrue(u1.password_hash != u2.password_hash)
