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
        self.fail('Finish the test!')

#She is invited to enter a to-do item straight away

#she types something and hits enter
#then the page updates and her text is on the page

#There is still a box if she wants to add another item

#The page updates again and shows both items

#Then a url is generated for her

#And then she quites the page
if __name__ == '__main__':
    unittest.main(warnings='ignore')
