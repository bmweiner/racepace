"""Conversions based on time and distance."""

import re

# meters for a given distance
DISTANCE = {
    'mile':1609.344,
    'kilometer':1000.0,
    'kay':1000.0,
    'meter':1.0,
    'yard':0.9144,
    'marathon':42164.8128,
    'half marathon':21082.4064,
}

# seconds for a given time
TIME = {
    'day':86400.0,
    'hour':3600.0,
    'minute':60.0,
    'second':1.0,
}

def trim_char(label, char='s'):
    """Trim char if exists."""
    if label.endswith(char):
        label = label[:-len(char)]
    return label.lower()

def add_char(label, char='s'):
    """Add char if does not exist."""
    if not label.endswith(char):
        label += char
    return label.lower()

def to_meters(number, unit):
    """Convert to meters."""
    unit = trim_char(unit)
    return number * DISTANCE[unit]

def from_meters(number, unit):
    """Convert from meters."""
    unit = trim_char(unit)
    return number / DISTANCE[unit]

def to_seconds(number, unit):
    """Convert to seconds."""
    unit = trim_char(unit)
    return number * TIME[unit]

def from_seconds(number, unit):
    """Convert from meters."""
    unit = trim_char(unit)
    return number / TIME[unit]

def from_duration(iso):
    """Convert ISO duration to seconds."""
    pat = ("P(?:(?P<year>\d*)Y)?"
           "(?:(?P<month>\d*)M)?"
           "(?:(?P<day>\d*)D)?"
           "T?(?:(?P<hour>\d*)H)?"
           "(?:(?P<minute>\d*)M)?"
           "(?:(?P<second>\d*)S)?")

    duration = re.search(pat, iso).groupdict(0)
    duration = {k:int(v) for k,v in duration.items()}
    total = 0

    total += duration['year'] * 365 * 24 * 60 * 60
    total += duration['month'] * 365/12 * 24 * 60 * 60
    total += duration['day'] * 24 * 60 * 60
    total += duration['hour'] * 60 * 60
    total += duration['minute'] * 60
    total += duration['second']
    return total

def to_hms(s):
    """Convert seconds to (h,m,s)."""
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    h = int(h)
    m = int(m)
    s = int(s)
    return (h, m, s)

def to_hms_text(seconds):
    text = ''
    hms = to_hms(seconds)
    labels = ('hour', 'minute', 'second')
    items = [(val, lab) for val, lab in zip(hms, labels) if val > 0]
    for i, (val, lab) in enumerate(items):
        text += '{} {}'.format(val, lab)
        if val > 1:
            text += 's'
        if i != len(items) - 1:
            if len(items) > 2:
                text += ', '
            if len(items) == 2:
                text += ' and '
            elif i == len(items) - 2:
                text += 'and '
    return text

def to_number_text(val, ndigits = 2):
    val = round(val, ndigits)
    if val.is_integer():
        return str(int(val))
    else:
        return str(val)
