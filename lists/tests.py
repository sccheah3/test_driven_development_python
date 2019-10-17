from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

class HomePageTest(TestCase):
    def test_root_urls_resolves_to_home_page_view(self):
        found = resolve('/')    # resolve is the func Django uses internally
                                #   to resolve URLs and find what view func
                                #   they should map to. We are checking the '/'
                                #       find the function 'home_page'
        self.assertEqual(found.func, home_page)


