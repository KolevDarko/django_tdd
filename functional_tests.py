from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retreive_it_later(self):
    #User goes to the webpage
        self.browser.get('http://localhost:8000')

    #She notices the page title mentions todo lists
        self.assertIn('To-Do', self.browser.title)
    #Also the header mentions to do lists
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("To-Do", header_text)
    #She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'), 'Enter a to-do item')


    #she types "Buy peacock feathers" into a text box and hits enter
        inputbox.send_keys("Buy peacock feathers")
    #then the page updates and her text is on the page
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.fid_elements_by_tag_name('tr')
        self.assertTrue(
                any(row.text == '1: Buy peacock feathers' for row in rows)
                )
#There is still a box if she wants to add another item
        self.fail('Finish the test mfr')
#The page updates again and shows both items

#Then a url is generated for her

#And then she quites the page
if __name__ == '__main__':
    unittest.main(warnings='ignore')
