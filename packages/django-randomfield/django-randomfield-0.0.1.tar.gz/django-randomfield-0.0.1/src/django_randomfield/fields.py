""" Model field module."""

from django.db.models import CharField, IntegerField


class CharRandomField(CharField):
    pass


class IntegerRandomField(IntegerField):
    pass
