from django.db import models


class List(models.Model):
    """
    Description: List of Items
    """
    pass


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
