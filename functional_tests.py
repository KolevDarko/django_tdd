from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retreive_it_later(self):

        # User goes to the webpage
        self.browser.get('http://localhost:8000')

    # She notices the page title mentions todo lists
        self.assertIn('To-Do', self.browser.title)
    # Also the header mentions to do lists
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("To-Do", header_text)
    # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

    # she types "Buy peacock feathers" into a text box and hits enter
        inputbox.send_keys("Buy peacock feathers")
    # then the page updates and her text is on the page
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy peacock feathers')
# There is still a box if she wants to add another item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feather to make a fly')
        inputbox.send_keys(Keys.ENTER)

# The page updates again and shows both items
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: User peacocks to make a fly')

# Then a url is generated for her
        self.fail('Finish the test lion')
# And then she quites the page
if __name__ == '__main__':
    unittest.main(warnings='ignore')
