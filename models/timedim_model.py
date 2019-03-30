import arrow
from django.db import models


class TimeDim(models.Model):
    """
    The Time Dimension
    """

    # Fields
    time_actual = models.TimeField()
    hour = models.PositiveSmallIntegerField(max_length=2)
    hour_str = models.CharField(max_length=2)
    military_hour = models.PositiveSmallIntegerField(max_length=2)
    military_hour_str = models.CharField(max_length=2)
    minute = models.PositiveSmallIntegerField(max_length=2)
    minute_str = models.CharField(max_length=2)
    minute_of_day = models.PositiveSmallIntegerField(max_length=1440)
    am_pm = models.CharField(max_length=2)

    objects = TimeDimManager()

    class Meta:
        ordering = ('minute_of_day',)

    def __str__(self):
        return f'{self.hour_str}:{self.minute_str} {self.am_pm}'

    def as_arrow(self, tz='utc'):
        return arrow.get(self.time_actual).to(tz)
