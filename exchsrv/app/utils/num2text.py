#!python
#cython: language_level=3, always_allow_keywords=True
from decimal import Decimal

int_units = ((u'рубль', u'рубля', u'рублей'), 'm')
exp_units = ((u'копейка', u'копейки', u'копеек'), 'f')

units = (
    u'ноль',
    (u'один', u'одна'),
    (u'два', u'две'),
    u'три', u'четыре', u'пять',
    u'шесть', u'семь', u'восемь', u'девять'
)

teens = (
    u'десять', u'одиннадцать',
    u'двенадцать', u'тринадцать',
    u'четырнадцать', u'пятнадцать',
    u'шестнадцать', u'семнадцать',
    u'восемнадцать', u'девятнадцать'
)

tens = (
    teens,
    u'двадцать', u'тридцать',
    u'сорок', u'пятьдесят',
    u'шестьдесят', u'семьдесят',
    u'восемьдесят', u'девяносто'
)

hundreds = (
    u'сто', u'двести',
    u'триста', u'четыреста',
    u'пятьсот', u'шестьсот',
    u'семьсот', u'восемьсот',
    u'девятьсот'
)

orders = (
    ((u'', u'', u''), 'm'),
    ((u'рубль', u'рубля', u'рублей'), 'm'),
    ((u'копейка', u'копейки', u'копеек'), 'f'),
    ((u'тысяча', u'тысячи', u'тысяч'), 'f'),
    ((u'миллион', u'миллиона', u'миллионов'), 'm'),
    ((u'миллиард', u'миллиарда', u'миллиардов'), 'm'),
)

minus = u'минус'


def thousand(rest, sex):
    prev = 0
    plural = 2
    name = []
    use_teens = 10 <= rest % 100 <= 19
    if not use_teens:
        data = ((units, 10), (tens, 100), (hundreds, 1000))
    else:
        data = ((teens, 10), (hundreds, 1000))
    for names, x in data:
        cur = int(((rest - prev) % x) * 10 / x)
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(teens[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                name_ = name_[0 if sex == 'm' else 1]
            name.append(name_)
            if 2 <= cur <= 4:
                plural = 1
            elif cur == 1:
                plural = 0
            else:
                plural = 2
        else:
            name.append(names[cur-1])
    return plural, name


def num2text(num, main_units=((u'', u'', u''), 'm')):
    _orders = (main_units,) + orders
    if num == 0:
        return ' '.join((units[0], _orders[0][0][2])).strip()

    rest = abs(num)
    ordr = 0
    name = []
    while rest > 0:
        plural, nme = thousand(rest % 1000, _orders[ordr][1])
        if nme or ordr == 0:
            name.append(_orders[ordr][0][plural])
        name += nme
        rest = int(rest / 1000)
        ordr += 1
    if num < 0:
        name.append(minus)
    name.reverse()
    return ' '.join(name).strip()


def decimal2text(value, places=2,
                 intunits=(('', '', ''), 'm'),
                 expunits=(('', '', ''), 'm')):
    value = Decimal(value)
    q = Decimal(10) ** -places

    integral, exp = str(value.quantize(q)).split('.')
    return u'{} {}'.format(
        num2text(int(integral), intunits),
        num2text(int(exp), expunits))
