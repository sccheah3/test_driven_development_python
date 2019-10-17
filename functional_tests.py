from selenium import webdriver
import unittest

# 1. Tests are organized into classes, which inherit from "unittest.TestCase"
# 2. main body of test is "test_can_start_a_list_and_retrieve_it_later". Any method
#		that starts with 'test' is a test method, and will be run by the test runner.
#		You can have more than one test method per class
# 3. setUp() and tearDown() will run even if there's an error during the test itself. 
#		No more firefox window lying around at the end
# 4. we use self.assertIn instead of just 'assert' to make our test assertions.
#		unittest provides lots of helper functions like this to make test assertions, like
#		assertEqual, assertTrue, assertFalse
# 5. self.fail just fails no matter what, producing the error message given. 
#		Using it as reminder to finis the test


class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# check out homepage
		self.browser.get('http://localhost:8000')

		# check todo is in page title
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!')

		# field exists to enter to-do item

		# enters "Buy peacock feathers"
		# page will update after entering
		# page now lists "1: Buy peacock feathers" as an item in todo list

		# another text box exists still
		# enters: "Use peacock feathers to make a fly"

		# visit url again - list still exists

		# exit site
		browser.quit()

if __name__ == "__main__":
	unittest.main()