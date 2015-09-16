from django.test import TestCase

from lists.forms import ItemForm, EMPTY_LIST_ERROR


class ItemFormTest(TestCase):

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save()