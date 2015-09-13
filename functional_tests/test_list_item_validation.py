from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ValidationsTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        error_text = self.browser.find_element_by_css_selector(
            '.has-error').text
        self.assertEqual(error_text, 'Cannot have empty list item')

        # She tries again with some text for the item, which now works
        self.browser.find_element_by_id('id_new_item').send_keys(
            'Buy cheese\n')
        self.check_for_row_in_list_table('1: Buy cheese')

        # Perversely, she now decides to submit a second blank list item
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Buy cheese')
        error_text = self.browser.find_element_by_css_selector(
            '.has-error').text
        self.assertEqual(error_text, 'Cannot have empty list item')

        # And she can correct it by filling some text in
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy cheese')
        self.check_for_row_in_list_table('2: Make tea')