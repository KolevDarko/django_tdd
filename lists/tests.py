from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['new_item_text'] = 'A new list item'

        response = home_page(request)

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'})
        self.assertEquals(response.content.decode(), expected_html)
        self.assertIn('A new list item', response.content.decode())


class ItemModelTest(TestCase):
    """
    Testing the Item Model
    """
    def test_saving_and_retreiving_items(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second = Item()
        second.text = "The second ever"
        second.save()

        saved_items = Item.objects.all()
        self.assertEquals(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,
                         "The first (ever) list item")
        self.assertEqual(second_saved_item.text,
                         "The second ever")
