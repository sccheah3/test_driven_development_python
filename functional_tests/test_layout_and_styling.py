from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):
		# visit home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 500)

		# input box is centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + (inputbox.size['width'] / 2),
			512,
			delta=35
		)


		# start new list and see the input is nicely centered
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + (inputbox.size['width'] / 2),
			512,
			delta=35
		)
