import datetime

from django.utils import timezone
from django.test import TestCase

from .models import TestModel


class EpochDateTimeFieldTest(TestCase):
    """
    Custom Settings Test case where we need to dynamically create a test model
    that has the custom field we've created.
    We are testing the functionlity of this field.

    Basic CRUD using the custom field
    Lookups using the custom field, verifying data type of the custom field.

    """

    def setUp(self):
        self.date = timezone.make_aware(
            datetime.datetime(2012, 1, 1),
            timezone.get_default_timezone())

    def test_custom_field(self):
        token = TestModel.objects.create(
            id=1,
            test_field=self.date,
        )
        self.assertEqual(type(token.test_field), datetime.datetime)
        self.assertEqual(token.test_field, self.date)

    def test_get_by_customfield(self):
        TestModel.objects.create(
            id=1,
            test_field=self.date,
        )
        token = TestModel.objects.get(test_field=self.date)
        self.assertEqual(type(token.test_field), datetime.datetime)
        self.assertEqual(
            token.test_field,
            self.date
        )
