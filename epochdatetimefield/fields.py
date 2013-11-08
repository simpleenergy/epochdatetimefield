import datetime
import warnings

from django.db import models
from django import forms
from django.core import exceptions
from django.utils import timezone
from django.conf import settings

class EpochDateTimeField(models.Field):
    """
    EpochDateTimeField is a field that will take/return python datetime objects
    but store the values as integers (timestamps) in the database.

    The reasoning for this field is to allow for ease of use while writing python
    code and dealing with date times, but still not breaking backwards
    compatibility with the existing php api that still has to rely on this database.
    """

    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        """
        Returns the type of the value expected by the Database.
        """
        return 'BigIntegerField'

    def to_python(self, value):
        """
        converts the value from the database to a python representation.
        """
        if isinstance(value, datetime.datetime) or value is None:
            return value

        try:
            value = str(value)
        except ValueError:
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

        try:
            if len(value) == 13:
                value = float(value) / 1000.
            elif len(value) == 12:
                value = float(value) / 100.
            elif len(value) == 11:
                value = float(value) / 10.
            else:
                value = float(value)

            return timezone.make_aware(
                datetime.datetime.fromtimestamp(value),
                timezone.get_default_timezone())

        except ValueError:
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def get_prep_value(self, value):
        """
        For backwards compatibility, interpret naive datetimes in local
        time. This won't work during DST change, but we can't do much
        about it, so we let the exceptions percolate up the call stack.
        """
        value = super(EpochDateTimeField, self).get_prep_value(value)
        if value is not None and settings.USE_TZ and timezone.is_naive(value):
            warnings.warn("DateTimeField received a naive datetime (%s)"
                          " while time zone support is active." % value,
                          RuntimeWarning)
            default_timezone = timezone.get_default_timezone()
            value = timezone.make_aware(value, default_timezone)
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Casts datetimes into the format expected by the backend
        """
        return float(value.strftime("%s"))

    def formfield(self, **kwargs):
        """
        When using django forms, lets use a datetime field.
        """
        defaults = {'form_class': forms.DateTimeField}
        defaults.update(kwargs)
        return super(EpochDateTimeField, self).formfield(**defaults)

    def get_prep_lookup(self, lookup_type, value):
        """
        For dates lookups, convert the value to an int
        so the database backend always sees a consistent type.
        """
        if lookup_type in ('year', 'month', 'day', 'week_day', 'hour', 'minute', 'second'):
            raise TypeError('Lookup type %r not supported.' % lookup_type)
        return super(EpochDateTimeField, self).get_prep_lookup(lookup_type, value)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(rules=[], patterns=[r'^epochdatetimefield.fields\.EpochDateTimeField$'])
except ImportError:
    pass

