import datetime

import pytz
from django.db import models


class TimeDimQuerySet(models.QuerySet):
    def morning(self, tz='utc'):
        noon = datetime.time(12, 0).replace(tzinfo=pytz.timezone(tz))
        return self.filter(
            time_actual__lt=noon,
        )

    def afternoon(self, tz='utc'):
        noon = datetime.time(12, 0).replace(tzinfo=pytz.timezone(tz))
        evening = datetime.time(18, 0).replace(tzinfo=pytz.timezone(tz))
        return self.filter(
            time_actual__gt=noon,
            time_actual__lt=evening
        )

    def evening(self, tz='utc'):
        evening = datetime.time(18, 0).replace(tzinfo=pytz.timezone(tz))
        return self.filter(
            time_actual__gte=evening
        )


class TimeDimManager(models.Manager):
    def get_queryset(self):
        return TimeDimQuerySet(self.model, using=self._db)

    def morning(self, tz='utc'):
        return self.get_queryset().morning(tz)

    def afternoon(self, tz='utc'):
        return self.get_queryset().afternoon(tz)

    def evening(self, tz='utc'):
        return self.get_queryset().evening(tz)

    def get_hour_str(self, h: int) -> str:
        """

        :param h:
        :return:
        """
        if h < 10:
            return f'0{h}'
        return f'{h}'

    def get_minute_str(self, m: int) -> str:
        """

        :param m:
        :return:
        """
        if m < 10:
            return f'0{m}'
        return f'{m}'

    def time_exists(self, *, h: int, m: int) -> bool:
        """

        :param h:
        :param m:
        :return:
        """
        try:
            return self.get(
                hour=h,
                minute=m
            )
        except self.model.DoesNotExist:
            return False

    def create(self, *, h: int, m: int):
        """

        :param h:
        :param m:
        :return:
        """
        time_exists = self.time_exists(h=h, m=m)
        if time_exists:
            return time_exists

        time_actual = datetime.time(h, m)
        hour = h
        minute = m
        hour_str = time_actual.strftime("%H")
        hour_12 = int(time_actual.strftime("%I"))
        hour_12_str = int(time_actual.strftime("%I"))
        minute_str = time_actual.strftime("%M")
        minute_of_day = (datetime.timedelta(hours=time_actual.hour, minutes=time_actual.minute) - datetime.timedelta(
            hours=0, minutes=0)).seconds // 60
        am_pm = time_actual.strftime("%p")

        t = super(TimeDimManager, self).create(
            time_actual=time_actual,
            hour=hour,
            minute=minute,
            hour_str=hour_str,
            hour_12=hour_12,
            hour_12_str=hour_12_str,
            minute_str=minute_str,
            minute_of_day=minute_of_day,
            am_pm=am_pm,
        )

        return t

    def bootstrap(self):
        for h in range(0, 24):
            for m in range(0, 60):
                t = self.create(h=h, m=m)
                print(f"Bootstrapping {t}")
