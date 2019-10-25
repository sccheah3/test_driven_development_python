from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page

from lists.models import Item, List

# uses test client which is a python class that acts as a dummy Web browser,
#   allowing us to test views and interact with app programatically 
#  Able to simulate GET and POST req on a URL and observe response
#   see chain of redirects and check the URL and status code at each step
#   Test that a given req is rendered by a specific django template, with a template context
#       that contains certain values

# Not to be used as a replacement for selenium. Django's test client has diff focus:
#   use Django test client to est that correct template is rendered and that the template
#       is passed the correct context data
#   Use in-browser frameworks like selenium to test RENDERED HTML and the BEHAVIOR
#       of the web pages. LiveServerTestCase provides support for this


#  each individual test method is wrapped in an atomic block, 
#	and each atomic block is rolled back at the end of the test method, 
#	this is expected behaviour. Django does this to ensure that tests are isolated, 
#	making it easier to find any problems when they occur.
#  The DB rolls back after each test method so its a clean Db for each test method
#		it helps with isolation

class HomePageTest(TestCase):

	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	# def test_only_saves_items_when_necessary(self):
	# 	self.client.get('/')
	# 	self.assertEqual(Item.objects.count(), 0)

	# def test_displays_all_list_items(self):
	# 	Item.objects.create(text='itemey 1')
	# 	Item.objects.create(text='itemey 2')

	# 	response = self.client.get('/')

	# 	self.assertIn('itemey 1', response.content.decode())
	# 	self.assertIn('itemey 2', response.content.decode())

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

		
#class ItemModelTest(TestCase):
class ListAndItemModelsTest(TestCase):

	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()

		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]

		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
	def test_uses_list_template(self):
		list_ = List.objects.create()
		item = Item.objects.create(text="hi", list=list_)

		response = self.client.get(f'/lists/{list_.id}/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)

		other_list = List.objects.create()
		Item.objects.create(text="other list item 1", list=other_list)
		Item.objects.create(text="other list item 2", list=other_list)

		response = self.client.get(f'/lists/{correct_list.id}/')


		# list_ = List.objects.create()
		# list_.item_set.create(text='itemey 1')
		# list_.item_set.create(text='itemey 2')

		# response = self.client.get('/lists/the-only-list-in-the-world/')

		# self.assertIn('itemey 1', response.content.decode())
		# self.assertIn('itemey 2', response.content.decode())
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')

		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')


class NewListTest(TestCase):
	def test_can_save_a_POST_request(self):
		self.client.post('/lists/new', data={'item_text': 'A new list item'})

		self.assertEqual(Item.objects.count(), 1)

		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

		# self.assertIn('A new list item', response.content.decode())
		# self.assertTemplateUsed(response, 'home.html')

	def test_redirects_after_POST(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'}) 
		new_list = List.objects.first()

		# self.assertEqual(response.status_code, 302)
		# self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
		self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):
	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			f'/lists/{correct_list.id}/add_item',
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			f'/list/{correct_list.id}/add_item',
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertRedirects(response, f'/lists/{correct_list.id}')