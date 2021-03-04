from unittest import main, TestCase
from unittest.mock import patch

from models.user import User


class Test(TestCase):

    def setUp(self) -> None:
        self.test = User(username="test name", password="test_password",
                         unique_id="some unique id", id=20)

    def tearDown(self) -> None:
        pass

    def test___init__(self):
        test = User(username="test name", password="test_password",
                    unique_id="some unique id", id=20)

        self.assertEqual(test.username, "test name")
        self.assertEqual(test.password, "test_password")
        self.assertEqual(test.unique_id, "some unique id")
        self.assertEqual(test.id, 20)

    def test_hash_password(self):
        hashed_password = User.hash_password(password="test_password")
        hashed_password_two = User.hash_password(password="test_password")

        self.assertNotEqual(hashed_password, hashed_password_two)

    @patch("models.user.check_password_hash")
    def test_check_password(self, mock_check_password):
        result = self.test.check_password(password="another checked password")

        mock_check_password.assert_called_once_with("test_password", "another checked password")
        self.assertEqual(mock_check_password.return_value, result)

    @patch("models.user.random.randint")
    def test_save_instance(self, mock_randint):
        expected_outcome = f"TE{mock_randint.return_value}"
        self.assertEqual(expected_outcome, self.test._generate_unique_id())
        mock_randint.assert_called_once_with(3, 900)

    @patch("models.user.DbEngine")
    @patch("models.user.User._generate_unique_id")
    @patch("models.user.User.hash_password")
    def test_save_instance(self, mock_hash_password, mock__generate_unique_id, mock_db_engine):
        self.test.save_instance()

        mock_hash_password.assert_called_once_with(password="test_password")
        mock__generate_unique_id.assert_called_once_with()
        mock_db_engine.assert_called_once_with()
        mock_db_engine.return_value.session.add.assert_called_once_with(self.test)
        mock_db_engine.return_value.session.commit.assert_called_once_with()


if __name__ == "__main__":
    main()
