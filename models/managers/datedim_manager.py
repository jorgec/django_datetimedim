import calendar
import datetime
from typing import List, Tuple

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
    def get_first_day_of_quarter(d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        quarter_idx = d.month // 4
        first_month = QUARTER_STARTS[quarter_idx]
        return datetime.date(
            d.year,
            first_month,
            1
        )

    @staticmethod
    def get_last_day_of_quarter(d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        quarter_idx = d.month // 4
        last_month = QUARTER_STARTS[quarter_idx] + 2
        return datetime.date(
            d.year,
            last_month,
            calendar.monthrange(d.year, last_month)[1]
        )

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
    def get_week(d: datetime.date, week_starts_on: int = calendar.MONDAY) -> Tuple[List[datetime.date], int]:
        """
        Returns tuple containing a list of dates of that week, and an integer denoting the week in month number
        :param d:
        :param week_starts_on:
        :return:
        """
        weeks = calendar.Calendar(week_starts_on).monthdatescalendar(d.year, d.month)
        i = 1
        for week in weeks:
            if d in week:
                return week, i
            i += 1

    def get_week_of_month(self, d: datetime.date, week_starts_on: int = calendar.MONDAY) -> int:
        return self.get_week(d)[1]

    @staticmethod
    def get_quarter_name(quarter: int):
        return QUARTER_NAMES[quarter]

    def get_first_day_of_week(self, d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        return self.get_week(d)[0][0]

    def get_last_day_of_week(self, d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        return self.get_week(d)[0][-1]

    @staticmethod
    def get_first_day_of_month(d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        return datetime.date(d.year, d.month, 1)

    @staticmethod
    def get_last_day_of_month(d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        return datetime.date(
            d.year,
            d.month,
            calendar.monthrange(d.year, d.month)[1]
        )

    @staticmethod
    def check_is_weekend(d: datetime.date) -> bool:
        """

        :param d:
        :return:
        """
        return d.isocalendar()[2] == 6 or d.isocalendar()[2] == 7

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

    def bootstrap(self, years: List[int], week_starts_on: int = calendar.MONDAY) -> None:
        calendar.setfirstweekday(week_starts_on)
        for year in range(years[0], years[1] + 1):
            for month in range(1, 13):
                num_days = calendar.monthrange(year, month)[1]
                for day in range(1, num_days + 1):
                    d = self.create(
                        year=year,
                        month=month,
                        day=day,
                        week_starts_on=week_starts_on
                    )
                    print(f"Bootstrapping {d}...")

    def create(self, *, year: int, month: int, day: int, week_starts_on: int = calendar.MONDAY):
        """

        :param year:
        :param month:
        :param day:
        :param week_starts_on:
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
            week_of_month = self.get_week_of_month(date_actual, week_starts_on)
            week_of_year = date_actual.isocalendar()[1]
            month_name = calendar.month_name[month]
            month_abbr = calendar.month_abbr[month]
            month_str = self.get_month_str(date_actual)
            first_day_of_week = self.get_first_day_of_week(date_actual)
            last_day_of_week = self.get_last_day_of_week(date_actual)
            first_day_of_month = self.get_first_day_of_month(date_actual)
            last_day_of_month = self.get_last_day_of_month(date_actual)
            first_day_of_quarter = self.get_first_day_of_quarter(date_actual)
            last_day_of_quarter = self.get_last_day_of_quarter(date_actual)
            first_day_of_year = datetime.date(date_actual.year, 1, 1)
            last_day_of_year = datetime.date(date_actual.year, 12, 31)
            year_actual_iso, week_iso, week_date_iso = date_actual.isocalendar()
            is_weekend = self.check_is_weekend(date_actual)

            d = super(DateDimManager, self).create(
                day=day,
                day_str=day_str,
                date_actual=date_actual,
                epoch=epoch,
                day_name=day_name,
                day_abbr=day_abbr,
                day_of_week=day_of_week,
                day_of_month=day_of_month,
                day_of_quarter=day_of_quarter,
                day_of_year=day_of_year,
                week_of_month=week_of_month,
                week_of_year=week_of_year,
                month=month,
                month_str=month_str,
                month_name=month_name,
                month_abbr=month_abbr,
                quarter=quarter,
                quarter_name=quarter_name,
                year=year,
                first_day_of_week=first_day_of_week,
                last_day_of_week=last_day_of_week,
                first_day_of_month=first_day_of_month,
                last_day_of_month=last_day_of_month,
                first_day_of_quarter=first_day_of_quarter,
                last_day_of_quarter=last_day_of_quarter,
                first_day_of_year=first_day_of_year,
                last_day_of_year=last_day_of_year,
                is_weekend=is_weekend,
                year_actual_iso=year_actual_iso,
                week_iso=week_iso,
                week_date_iso=week_date_iso,
            )

            return d
