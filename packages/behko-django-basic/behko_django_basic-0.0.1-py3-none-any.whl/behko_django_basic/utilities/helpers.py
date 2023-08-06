from typing import Callable, Union, List

from django.urls import path
from django.urls.conf import include as django_include


def uwrap(urls, app_name="free"):
    return urls, app_name,


def include(urls, namespace, app_name="free"):
    return django_include(uwrap(urls, app_name), namespace=namespace)


def set_first_parameter(func, *args, **kwargs):
    def afunc(*args1, **kwargs1):
        return func(*args, *args1, **kwargs, **kwargs1)

    return afunc


class FieldController:

    def __init__(self, fields=None, field=None):
        self.fields = fields
        self.field = field

    def get_one(self, *args):
        fields = self.get_field_names()
        output = args[-1]
        for i in args[:-1]:
            output.append(FieldController(self.fields, fields[i]))
        return self

    def get_field(self, index=None):
        fields = self.get_field_names()
        return [self.fields[field] for field in fields]

    def get_field_names(self):
        if isinstance(self.field, str):
            fields = [self.field]
        else:
            fields = self.field
        return fields

    def set_css_class(self, classes):
        for field in self.get_field():
            field.widget.attrs = {"class": ' '.join(classes)}
        return self

    def add_css_class(self, classes):
        for field in self.get_field():
            field.widget.attrs.update({"class": ' '.join(classes)})
        return self

    def set_field_attr(self, attr, value):
        for field in self.get_field():
            setattr(field, attr, value)
        return self

    def add_field_attr(self, attr, value):
        for field in self.get_field():
            field.widget.attrs.update({attr: value})
        return self

    @property
    def f(self):
        return self.get_field()


def gfc(fields, key):
    f = FieldController()
    f.fields = fields
    f.field = key
    return f


class GFCMixin:
    @property
    def g(self) -> Callable[[Union[str, List[str]]], FieldController]:
        return set_first_parameter(gfc, self.fields)


def create_all_in_one(all_in_one, other, namespace=None):
    all_in_one = all_in_one()

    if all_in_one.namespace is None and namespace is None:
        raise Exception('Please Specify namespace for %s' % all_in_one.__class__)

    return include([
        path('create/', all_in_one.get_create_class().as_view(), name='create'),
        path('delete/<int:pk>', all_in_one.get_delete_class().as_view(), name='delete'),
        path('update/<int:pk>', all_in_one.get_update_class().as_view(), name='update'),
        path('datatable/', all_in_one.get_datatable_class().as_view(), name='datatable'),
        *other
    ], namespace=all_in_one.namespace or namespace)
