__author__ = 'darko'
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()

from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest

class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
#        to set a cookie first need to visit page
#       404 loads fastest
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def test_logged_in_ussers_lists_are_saved_as_my_lists(self):
        email = 'darko@example.com'

        self.browser.get(self.server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged user
        self.create_pre_authenticated_session(email)

        self.browser.get(self.server_url)
        self.wait_to_be_logged_in(email)
