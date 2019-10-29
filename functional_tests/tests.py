from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
	# setup and teardown are executed before and after each test method
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


	def test_can_start_a_list_for_one_user(self):
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


	def test_multiple_users_can_start_lists_at_different_urls(self):
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# list has unique url
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')


		# new user
		# use new browser session to make sure that no info from prev
		# user is coming through fro mcookies etc
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# new user visits homepage. 
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# user gets own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		# there is no trace of ediths list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

