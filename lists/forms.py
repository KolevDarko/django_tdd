from django.core.exceptions import ValidationError
from django import forms
from lists.models import Item


EMPTY_LIST_ERROR = "Cannot have empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"


class ItemForm(forms.models.ModelForm):

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    # is_valid to work, I need to override validate_unique
    # that's one way though, I guess
    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            # Take the error and set our custom message
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            # Then insert it back in django
            self._update_errors(e)
