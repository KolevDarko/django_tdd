from unittest import skip

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class ItemModelTest(TestCase):
    """
    Testing the Item Model
    """
    def test_saving_and_retreiving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second = Item()
        second.text = "The second ever"
        second.list = list_
        second.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEquals(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text,
                         "The first (ever) list item")
        self.assertEquals(first_saved_item.list, list_)

        self.assertEqual(second_saved_item.text,
                         "The second ever")
        self.assertEquals(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_display_items_for_one_list(self):
        correct_one = List.objects.create()
        item1 = Item.objects.create(text="test1", list=correct_one)
        item2 = Item.objects.create(text="test2", list=correct_one)

        wrong_one = List.objects.create()
        item12 = Item.objects.create(text="test12", list=wrong_one)
        item22 = Item.objects.create(text="test22", list=wrong_one)

        response = self.client.get('/lists/%d/' % (correct_one.id))

        self.assertContains(response, item1.text)
        self.assertContains(response, item2.text)
        self.assertNotContains(response, item12.text)
        self.assertNotContains(response, item22.text)

    def test_passes_correct_list_to_template(self):
        List.objects.create()
        my_list = List.objects.create()

        response = self.client.get('/lists/%d/' % (my_list.id))

        self.assertEquals(response.context['list'].id, my_list.id)


class NewListTest(TestCase):

    def test_saving_a_post_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        last_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (last_list.id))

    @skip
    def test_throws_error_on_empty_item(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': ''}
        )
        self.assertEquals(response.context['errors'],
                          'Cannot submit empty item')
        self.assertTemplateUsed(response, 'home.html')


class NewItemTest(TestCase):

    def test_adds_new_item_to_list(self):
        list_ = List.objects.create()
        Item.objects.create(text="basdf", list=list_)
        response = self.client.post(
            '/lists/%d/add_item' % (list_.id),
            data={'item_text': 'Item list in old list'}
        )
        item = Item.objects.first()
        self.assertEqual(Item.objects.filter(list=list_).all().count(), 2)
        self.assertEqual(item.list, list_)
        self.assertRedirects(response, '/lists/%d/' % (list_.id))

    def test_redirects_to_list_view(self):
        List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
