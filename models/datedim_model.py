import arrow

from django.db import models

from datetimedim.models.managers import DateDimManager


class DateDim(models.Model):
    """
    The Date Dimension
    """

    # Fields
    day = models.PositiveSmallIntegerField()
    day_str = models.CharField(max_length=2)
    date_actual = models.DateField()
    epoch = models.PositiveIntegerField(unique=True)
    day_name = models.CharField(max_length=9)
    day_abbr = models.CharField(max_length=3)
    day_of_week = models.PositiveSmallIntegerField()
    day_of_month = models.PositiveSmallIntegerField()
    day_of_quarter = models.PositiveSmallIntegerField()
    day_of_year = models.PositiveSmallIntegerField()
    week_of_month = models.PositiveSmallIntegerField()
    week_of_year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    month_str = models.CharField(max_length=2)
    month_name = models.CharField(max_length=9)
    month_abbr = models.CharField(max_length=3)
    quarter = models.PositiveSmallIntegerField()
    quarter_name = models.CharField(max_length=9)
    year = models.PositiveSmallIntegerField()
    first_day_of_week = models.DateField()
    last_day_of_week = models.DateField()
    first_day_of_month = models.DateField()
    last_day_of_month = models.DateField()
    first_day_of_quarter = models.DateField()
    last_day_of_quarter = models.DateField()
    first_day_of_year = models.DateField()
    last_day_of_year = models.DateField()
    is_weekend = models.BooleanField(default=False)
    year_actual_iso = models.PositiveSmallIntegerField()
    week_iso = models.CharField(max_length=10)
    week_date_iso = models.CharField(max_length=12)
    ordinal_iso = models.CharField(max_length=8)


    objects = DateDimManager()

    class Meta:
        ordering = ('-date_actual',)
        unique_together = ('day', 'month', 'year')

    def __str__(self):
        return self.date_actual.isoformat()

    def as_arrow(self):
        return arrow.get(self.date_actual)
