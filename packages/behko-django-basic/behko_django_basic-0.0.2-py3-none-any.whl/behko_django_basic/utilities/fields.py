from datetime import timezone, datetime

import pytz
from behko_django_basic.converter import change_date_to_persian, change_date_to_english
from django.forms import forms, DateTimeInput, DateTimeField


class ConvertDatetimeInput(DateTimeInput):

    def format_value(self, value):
        if value is not None and isinstance(value, datetime):
            value = value.replace(tzinfo=timezone.utc).astimezone(pytz.timezone("Asia/Tehran"))
            value = change_date_to_persian(value, p_numbers=True)
        return value


class ConvertDatetime(DateTimeField):
    widget = ConvertDatetimeInput
    default_error_messages = {
        'invalid': 'لطفاً تاریخ صحیحی را وارد کنید',
    }

    def clean(self, value):
        if isinstance(value, str):
            value = change_date_to_english(value, 2)
        data = super().clean(value)
        return data
