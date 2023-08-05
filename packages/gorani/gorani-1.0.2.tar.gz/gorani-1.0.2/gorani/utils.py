from datetime import timedelta, tzinfo
from dateutil.parser import parse
import datetime
import time
import numpy as np
import calendar

ZERO = timedelta(0)

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()

class Zone(tzinfo):
    def __init__(self, offset, isdst, name):
        self.offset = offset
        self.isdst = isdst
        self.name = name

    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)

    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)

    def tzname(self, dt):
        return self.name

kst = Zone(9, False, "KST")

def to_timestamp(x):
    return int(time.mktime(x.timetuple()))

def parse_ts(s):
    return calendar.timegm(parse(str(s)).utctimetuple())

def parse_date(s):
    return datetime.datetime.fromtimestamp(s).strftime('%m/%d')


def split_sentence(sen):
    import re
    out = re.split("[^a-zA-Z-']+", sen)

    if out[0] == '':
        if len(out) == 1:
            return []
        out = out[1:]
    if out[len(out) - 1] == '':
        if len(out) == 1:
            return []
        out = out[:-1]
    return out

import pandas as pd

def unnesting(df, explode, axis=1):
    if axis==1:
        idx = df.index.repeat(df[explode[0]].str.len())
        df1 = pd.concat([
            pd.DataFrame({x: np.concatenate(df[x].values)}) for x in explode], axis=1)
        df1.index = idx

        return df1.join(df.drop(explode, 1), how='left')
    else:
        df1 = pd.concat([
                         pd.DataFrame(df[x].tolist(), index=df.index).add_prefix(x) for x in explode], axis=1)
        return df1.join(df.drop(explode, 1), how='left')