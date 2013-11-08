from django.db import models

from epochdatetimefield.fields import EpochDateTimeField


class TestModel(models.Model):
    """
    Test model for testing the EpochDateTimeField
    """
    test_field = EpochDateTimeField()
