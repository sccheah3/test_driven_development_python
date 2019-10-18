from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page

class HomePageTest(TestCase):
    def test_root_urls_resolves_to_home_page_view(self):
        found = resolve('/')    # resolve is the func Django uses internally
                                #   to resolve URLs and find what view func
                                #   they should map to. We are checking the '/'
                                #       find the function 'home_page'
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()         # we create an 'HttpRequest' object, which is what
                                        #   Django will see when a user's browser asks for a page
        response = home_page(request)   # Pass it to our home_page view, which gives us a response.
                                        #   This object is an instance of a class HttpResponse

        html = response.content.decode('utf8')  # Extract the .content of the response. These are
                                                #   raw bytes. We call .decode() to convert them into 
                                                #   the string of HTML that's being sent to the user
                                                        
        self.assertTrue(html.startswith('<html>'))  # Want to start with an <html> tag
        self.assertIn('<title>To-Do lists</title>', html) # we also want a <title> tag somewhere in
                                                          #     the middle with words "To-Do lists" 
                                                          #     b/c that's for our functional test
        self.assertTrue(html.endswith('</html>'))

