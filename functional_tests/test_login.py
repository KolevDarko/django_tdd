import time

from .base import FunctionalTest

from selenium.webdriver.support.ui import WebDriverWait
TEST_EMAIL = 'darko@mockmyid.com'

class LoginTest(FunctionalTest):

    def switch_to_new_window(self, title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to.window(handle)
                if title in self.browser.title:
                    return
            retries = -1
            time.sleep(0.5)
        self.fail('could not find window')

    def test_login_with_persona(self):
        # Edith goes to superlists site
        #  and notices a Sign In link for the first time
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # Edith logs in with her email address
        # Use mockmyid.com for test email
        self.browser.find_element_by_id('authentication_email'
            ).send_keys('darko@mockmyid.com')
        self.browser.find_element_by_tag_name('button').click()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # She can see that she is logged in
        self.wait_to_be_logged_in(TEST_EMAIL)

#        Refreshing the page, she sees  it's a real session login,
#        not just a one of for that page
        self.browser.refresh()
        self.wait_to_be_logged_in(TEST_EMAIL)

#       Then she clicks log out
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(TEST_EMAIL)
#
#       The logged out status also persists after refresh
        self.browser.refresh()
        self.wait_to_be_logged_out(TEST_EMAIL)

