from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()

from accounts.authentication import(
    PERSONA_VERIFY_URL, PersonaAuthenticationBackend
)


@patch('accounts.authentication.requests.post')
class AuthenticateTest(TestCase):

    def setUp(self):
        self.backend = PersonaAuthenticationBackend()
        user = User(email='default@test.com')
        user.username = 'default_user'
        user.save()

    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate('abc')
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={'assertion': 'abc', 'audience': settings.DOMAIN}
        )

    def test_returns_none_if_response_error(self, mock_post):
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}
        user = self.backend.authenticate('abc')
        self.assertIsNone(user)

    def test_returns_none_if_status_not_okay(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'not okay!'}
        user = self.backend.authenticate('abc')
        self.assertIsNone(user)

    def test_existing_user_with_email(self, mock_post):
        mock_post.return_value.json.return_value = {
            'status': 'okay', 'email': 'a@b.com'
        }
        actual_user = User.objects.create(email='a@b.com')
        found_user = self.backend.authenticate('an assertion')
        self.assertEqual(actual_user, found_user)

    def test_creates_new_user_if_necessary_for_valid_assertion(
        self, mock_post
    ):
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@b.com'}
        found_user = self.backend.authenticate('an assertion')
        created_user = User.objects.get(email='a@b.com')
        self.assertEqual(created_user, found_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        backend = PersonaAuthenticationBackend()
        other_user = User(email='other@user.com')
        other_user.username = 'other'
        other_user.save()
        desired_user = User.objects.create(email='a@b.com')
        found_user = backend.get_user('a@b.com')
        self.assertEqual(found_user, desired_user)

    def test_returns_none_if_no_user_with_that_email(self):
        backend = PersonaAuthenticationBackend()
        self.assertIsNone(
            backend.get_user('a@b.com')
        )
