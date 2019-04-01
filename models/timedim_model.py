import pytz
from django.db import models

from datetimedim.models.managers import TimeDimManager


class TimeDim(models.Model):
    """
    The Time Dimension
    """

    # Fields
    time_actual = models.TimeField(unique=True)
    hour = models.PositiveSmallIntegerField()
    hour_str = models.CharField(max_length=2)
    hour_12 = models.PositiveSmallIntegerField()
    hour_12_str = models.CharField(max_length=2)
    minute = models.PositiveSmallIntegerField()
    minute_str = models.CharField(max_length=2)
    minute_of_day = models.PositiveSmallIntegerField()
    am_pm = models.CharField(max_length=2)

    objects = TimeDimManager()

    class Meta:
        ordering = ('minute_of_day',)

    def __str__(self):
        return f'{self.hour_str}:{self.minute_str} {self.am_pm}'

    def tz_aware(self, tz='utc'):
        return self.time_actual.replace(tzinfo=pytz.timezone(tz))

    def tz_aware_12_str(self, fmt='%I:%M %p %Z %z', tz='utc'):
        return self.tz_aware(tz).strftime(fmt)

    def tz_aware_str(self, fmt='%H:%M %Z %z', tz='utc'):
        return self.tz_aware(tz).strftime(fmt)

    def as_12(self):
        return f'{self.hour_12_str}:{self.minute_str}'
