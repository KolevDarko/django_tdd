from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ValidationsTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        error_text = self.browser.find_element_by_css_selector(
            '.has-error').text
        self.assertEqual(error_text, 'Cannot have empty list item')

        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy cheese\n')
        self.check_for_row_in_list_table('1: Buy cheese')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)
        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Buy cheese')
        error_text = self.browser.find_element_by_css_selector(
            '.has-error').text
        self.assertEqual(error_text, 'Cannot have empty list item')

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy cheese')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies\n')

        # She sees a helpfull error message
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You've already got this in your list")
