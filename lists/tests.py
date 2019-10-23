from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page

from lists.models import Item


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

    # def test_home_page_returns_correct_html(self):
    #    request = HttpRequest()         # we create an 'HttpRequest' object, which is what
                                        #   Django will see when a user's browser asks for a page
    #    response = home_page(request)   # Pass it to our home_page view, which gives us a response.
                                        #   This object is an instance of a class HttpResponse

    #    response = self.client.get('/')
    #    self.assertTemplateUsed(response, 'home.html')

        # html = response.content.decode('utf8')  # Extract the .content of the response. These are
                                                #   raw bytes. We call .decode() to convert them into 
                                                #   the string of HTML that's being sent to the user
                                                        
        # self.assertTrue(html.startswith('<html>'))  # Want to start with an <html> tag
        # self.assertIn('<title>To-Do lists</title>', html) # we also want a <title> tag somewhere in
                                                          #     the middle with words "To-Do lists" 
                                                          #     b/c that's for our functional test
        # self.assertTrue(html.endswith('</html>'))

        
class ItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()

		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]

		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')