"""
Mixin to show changed fields per DRF resource.
"""
from django.forms import model_to_dict


class ChangedFieldsMixin(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__last_queryset = None

    def last_queryset(self):
        if not self.__last_queryset:
            self.__last_queryset = type(self).objects.get(pk=self.pk) if self.pk else None
        return self.__last_queryset

    def change_fields(self, *args):
        new = set(model_to_dict(self, args).items())
        if not self.pk:
            return list(dict(new).keys())

        old = set(model_to_dict(self.last_queryset(), args).items())
        return list(dict(new - old).keys())

    def save(self, *args, **kwargs):
        self.last_queryset()
        super().save(*args, **kwargs)
