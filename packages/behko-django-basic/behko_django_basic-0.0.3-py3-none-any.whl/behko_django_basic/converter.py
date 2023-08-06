import datetime

from django.utils import timezone
from unidecode import unidecode


def jalali_to_gregorian(jy, jm, jd):
    if (jy > 979):
        gy = 1600
        jy -= 979
    else:
        gy = 621
    if (jm < 7):
        days = (jm - 1) * 31
    else:
        days = ((jm - 7) * 30) + 186
    days += (365 * jy) + ((int(jy / 33)) * 8) + (int(((jy % 33) + 3) / 4)) + 78 + jd
    gy += 400 * (int(days / 146097))
    days %= 146097
    if (days > 36524):
        gy += 100 * (int(--days / 36524))
        days %= 36524
        if (days >= 365):
            days += 1
    gy += 4 * (int(days / 1461))
    days %= 1461
    if (days > 365):
        gy += int((days - 1) / 365)
        days = (days - 1) % 365
    gd = days + 1
    if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        kab = 29
    else:
        kab = 28
    sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while (gm < 13):
        v = sal_a[gm]
        if (gd <= v):
            break
        gd -= v
        gm += 1
    return [gy, gm, gd]


def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if (gy > 1600):
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = (365 * gy) + (int((gy2 + 3) / 4)) - (int((gy2 + 99) / 100)) + (int((gy2 + 399) / 400)) - 80 + gd + g_d_m[
        gm - 1]
    jy += 33 * (int(days / 12053))
    days %= 12053
    jy += 4 * (int(days / 1461))
    days %= 1461
    if (days > 365):
        jy += int((days - 1) / 365)
        days = (days - 1) % 365
    if (days < 186):
        jm = 1 + int(days / 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + int((days - 186) / 30)
        jd = 1 + ((days - 186) % 30)
    return [jy, jm, jd]


def change_date_to_english(value, mode=1):
    """
    برای تبدیل تاریخ شمسی به میلادی استفاده میشود
    تاریخ میلادی را دریافت میکند و تاریخ شمسی را در
    قالب رشته خروجی میدهد

    Arguments:
        value(str):
            تاریخ شمسی
        mode(int):
            حالت تبدیل را مشخص میکند
    """
    if value is None:
        return None
    if mode == 2:
        y, m, d = unidecode(value).split('/')
        pdate = jalali_to_gregorian(int(y), int(m), int(d))
        date_time = datetime.date(pdate[0], pdate[1], pdate[2])
        return date_time
    value = unidecode(value)
    stime, date = value.split(' ')
    stime = unidecode(stime)
    year, month, day = date.split('/')
    date = jalali_to_gregorian(int(year), int(month), int(day))
    string_date = "{y} {m} {d} ".format(y=date[0], m=date[1], d=date[2])
    string_date_time = string_date + stime
    date_time = datetime.datetime.strptime(string_date_time, "%Y %m %d %H:%M:%S")
    return date_time


def change_date_to_persian(value, mode=1, p_numbers=False):
    """
    برای تبدیل تاریخ میلادی به شمسی استفاده میشود
    تاریخ میلادی را دریافت میکند و تاریخ شمسی را در
    قالب رشته خروجی میدهد

    Arguments:
        value(str):
            تاریخ میلادی
        mtime(str):
            زمان
        mode(int):
            حالت تبدیل را مشخص میکند
    """
    if value is None:
        return None
    year = ""
    month = ""
    day = ""
    if isinstance(value, datetime.datetime) or isinstance(value, timezone):
        year, month, day = value.year, value.month, value.day
    elif mode == 2:
        value = str(unidecode(str(value)))
        year, month, day = value.split('-')
    date = gregorian_to_jalali(int(year), int(month), int(day))
    string_date = "{y}/{m}/{d}".format(y=date[0], m=date[1], d=date[2])
    if p_numbers:
        persian_numbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
        for p in persian_numbers:
            string_date = string_date.replace(str(int(p)), p)
    return string_date
