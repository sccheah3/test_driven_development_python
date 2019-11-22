from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		# go to homepage and submit an empty list item
		#	hit enter on empty input box

		# home page refresh, has an error message saying that 
		#	lsit items cannot be blank

		# try again with some text for the item, now works

		# try to submit second blank item

		# receives similar warning on the list page

		# correct by filling some text int
		self.fail('write me')