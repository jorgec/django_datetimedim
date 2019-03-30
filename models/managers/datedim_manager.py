import calendar
import datetime
import arrow
from django.db import models

from datetimedim.models.constants import QUARTER_STARTS, QUARTER_NAMES


class DateDimManager(models.Manager):

    @staticmethod
    def get_day_str(day: int) -> str:
        """
        Converts and pads day number
        :param day: int
        :return: str
        """
        if day < 10:
            return f'0{day}'
        return str(day)

    @staticmethod
    def get_epoch(d: datetime.date) -> int:
        """
        Get days since Jan 01, 0001
        :param d:
        :return: int
        """
        return d.toordinal()

    @staticmethod
    def get_day_name(d: datetime.date) -> str:
        """

        :param d:
        :return:
        """
        return calendar.day_name[calendar.weekday(d.year, d.month, d.day)]

    @staticmethod
    def get_day_abbr(d: datetime.date) -> str:
        """

        :param d:
        :return:
        """
        return calendar.day_abbr[calendar.weekday(d.year, d.month, d.day)]

    @staticmethod
    def get_day_of_week(d: datetime.date) -> int:
        """

        :param d:
        :return:
        """
        return d.isoweekday()

    @staticmethod
    def get_day_of_quarter(d: datetime.date) -> int:
        """

        :param d:
        :return:
        """
        quarter_idx = d.month // 4
        first_month = QUARTER_STARTS[quarter_idx]

        return (d.toordinal() - datetime.date(d.year, first_month, 1).toordinal()) + 1

    @staticmethod
    def get_day_of_year(d: datetime.date) -> int:
        """

        :param d:
        :return:
        """
        return (d.toordinal() - datetime.date(d.year, 1, 1).toordinal()) + 1

    @staticmethod
    def get_month_str(d: datetime.date) -> str:
        """

        :param d:
        :return:
        """
        if d.month < 10:
            return f'0{d.month}'
        return str(d.month)

    @staticmethod
    def get_quarter_name(quarter: int):
        return QUARTER_NAMES[quarter]

    @staticmethod
    def get_first_day_of_week(d: datetime.date):
        pass

    def date_exists(self, *, year: int, month: int, day: int):
        """
        Check whether date exists
        :param year: int
        :param month: int
        :param day: int
        :return: bool
        """

        try:
            return self.model.objects.get(
                year=year,
                month=month,
                day=day
            )
        except self.model.DoesNotExist:
            return False

    def create(self, *, year: int, month: int, day: int):
        """

        :param year:
        :param month:
        :param day:
        :return:
        """
        date_exists = self.date_exists(year=year, month=month, day=day)
        if date_exists:
            return date_exists
        else:
            date_actual = datetime.date(year=year, month=month, day=day)
            day_str = self.get_day_str(day)
            epoch = self.get_epoch(date_actual)
            day_name = self.get_day_name(date_actual)
            day_abbr = self.get_day_abbr(date_actual)
            day_of_week = self.get_day_of_week(date_actual)
            day_of_month = day
            quarter = (month // 4) + 1
            quarter_name = self.get_quarter_name(quarter)
            day_of_quarter = self.get_day_of_quarter(date_actual)
            day_of_year = self.get_day_of_year(date_actual)
            week_of_month = (date_actual.day // 7) + 1
            week_of_year = date_actual.isocalendar()[1]
            month_name = calendar.month_name(month)
            month_str = self.get_month_str(date_actual)
            first_day_of_week = self.get_first_day_of_week(date_actual)
