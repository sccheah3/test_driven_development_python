from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time
# import unittest

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


# Selenium provides several methods to examine web pages:
#	find_element_by_tag_name, find_element_by_id,
#	and find_elements_by_tag_name (returns several el)

# also use 'send_keys', which is seleniums way of typing into input elements

# 'Keys' class lets us send special keys like Enter

# When we hit enter, page will referesh. time.sleep is there to make sure
#	the browser has finished reloading before we make any assertions about the
#	new page. This is called an "explicit wait"

MAX_WAIT = 10

# class NewVisitorTest(unittest.TestCase):
class NewVisitorTest(LiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()

		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
			
				return
			except(AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e

				time.sleep(0.5)


	def test_can_start_a_list_and_retrieve_it_later(self):
		# check out homepage
		# self.browser.get('http://localhost:8000')
		# instead of hardcoding visit to localhost:8000, LiverServerTestCase gives
		#	an attribute called live_server_url
		self.browser.get(self.live_server_url)	

		# check todo is in page title
		self.assertIn('To-Do', self.browser.title)
		
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# check for input box
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# enters "Buy peacock feathers"
		inputbox.send_keys('Buy peacock feathers')

		# page will update after entering
		# page now lists "1: Buy peacock feathers" as an item in todo list
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers') 

		# There is still a text box inviting her to add another item. She 
		# enters "Use peacock feathers to make a fly" (Edith is very # methodical) 
		inputbox = self.browser.find_element_by_id('id_new_item') 
		inputbox.send_keys('Use peacock feathers to make a fly') 
		inputbox.send_keys( Keys.ENTER) 
		
		# The page updates again, and now shows both items on her list 
		self.wait_for_row_in_list_table('1: Buy peacock feathers') 
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly') 


		# another text box exists still
		# enters: "Use peacock feathers to make a fly"

		# visit url again - list still exists


		self.fail('Finish the test!')

		# exit site
		browser.quit()

# if __name__ == "__main__":
#	unittest.main()