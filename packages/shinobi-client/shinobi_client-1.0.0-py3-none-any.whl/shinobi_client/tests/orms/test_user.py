import unittest

from shinobi_client.api_key import ShinobiApiKey, ShinobiWrongPasswordError
from shinobi_client.orms.user import ShinobiUserOrm
from shinobi_client.tests._common import _create_email_and_password, TestWithShinobi


class TestShinobiUserOrm(TestWithShinobi):
    """
    Tests for `ShinobiUserOrm`.
    """
    def setUp(self):
        super().setUp()
        self.user_orm = ShinobiUserOrm(self._shinobi_client)
        self.api_key = ShinobiApiKey(self._shinobi_client)

    def test_create(self):
        email, password = _create_email_and_password()
        self.user_orm.create(email, password)
        user = self.user_orm.get(email)
        self.assertEqual(email, user["mail"])
        self.assertIsNotNone(self.api_key.get(email, password))

    def test_get_when_does_not_exist(self):
        user = self.user_orm.get("example@doesnotexist.com")
        self.assertIsNone(user)

    def test_get(self):
        user = self._create_user()
        retrieved_user = self.user_orm.get(user["email"])
        self.assertEqual(user["mail"], retrieved_user["mail"])

    def test_get_all(self):
        emails = []
        for i in range(3):
            emails.append(self._create_user()["mail"])

        matched_users = tuple(filter(lambda user: user["mail"] in emails, self.user_orm.get_all()))
        self.assertEqual(len(emails), len(matched_users))

    def test_modify_password_when_user_not_exist(self):
        email, password = _create_email_and_password()
        self.assertRaises(ValueError, self.user_orm.modify, email, password=password)

    def test_modify_password(self):
        user = self._create_user()
        _, password = _create_email_and_password()
        assert user["pass"] != password
        changed = self.user_orm.modify(user["email"], password=password)
        self.assertTrue(changed is None or changed is True)
        self.assertRaises(ShinobiWrongPasswordError, self.api_key.get, user["email"], user["pass"])
        self.assertIsNotNone(self.api_key.get(user["email"], password))

    def test_delete_when_user_not_exist(self):
        email, _ = _create_email_and_password()
        self.assertFalse(self.user_orm.delete(email))

    def test_delete(self):
        user = self._create_user()
        self.user_orm.delete(user["email"])
        self.assertIsNone(self.user_orm.get(user["email"]))


if __name__ == "__main__":
    unittest.main()
