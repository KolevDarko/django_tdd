from unittest import skip

from django.utils.html import escape
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List
from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_LIST_ERROR,
    ExistingListItemForm, ItemForm,
)


class HomePageTest(TestCase):
    maxDiff = None

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


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

    def test_can_save_a_post_request_to_an_existing_list(self):
        list_ = List.objects.create()
        Item.objects.create(text="basdf", list=list_)
        response = self.client.post(
            '/lists/%d/' % (list_.id),
            data={'text': 'Item list in old list'}
        )
        item = Item.objects.first()
        self.assertEqual(Item.objects.filter(list=list_).all().count(), 2)
        self.assertEqual(item.list, list_)
        self.assertRedirects(response, '/lists/%d/' % (list_.id))

    def test_post_redirects_to_list_view(self):
        List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % (list_.id),
            data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        error = 'Cannot have empty list item'
        self.assertContains(response, error)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            '/lists/%d/' % (list_.id,),
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_errors_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, EMPTY_LIST_ERROR)

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='key')
        response = self.client.post(
            '/lists/%d/' % (list1.id,),
            data={'text': 'key'})
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)


class NewListTest(TestCase):

    def test_saving_a_post_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )
        last_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (last_list.id))

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, EMPTY_LIST_ERROR)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_empty_items_arent_saved(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
