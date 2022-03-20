from django import template
from datetime import datetime

register = template.Library()


def convert_unix_date(date):
    return datetime.utcfromtimestamp(int(date))


register.filter('convert_unix_date', convert_unix_date)
