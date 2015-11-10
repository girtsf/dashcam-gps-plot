#!/usr/local/bin/python3
#
# Methods for parsing 0806 GPS format.

import collections
import logging
import os
import time

DataPoint = collections.namedtuple('DataPoint', 'timestamp lat lon speed')

# Raw entry parsed from comma-delimited log.
GpsLogEntry = collections.namedtuple('GpsLogEntry',
        'valid date time lat lat_dir lon lon_dir speed unknown acc1 acc2 acc3')


class Point:
    pass


def DmmToD(dmm, negative):
    """Converts coordinates from DDDMM.MMMMM to DD.DDDDDD.

    >>> DmmToD(1230.00, False)
    12.5
    >>> DmmToD(1245.00, True)
    -12.75
    """
    # 3744.5729   37  44.5729
    degrees = dmm // 100
    minutes = dmm - (degrees * 100)
    part = minutes / 60.0
    degrees_with_part = degrees + part
    if negative:
        degrees_with_part *= -1
    return degrees_with_part


def ParseLine(line):
    """Parses one line.

    >>> ParseLine('A,081015,183603.000,3744.6086,N,12224.3720,W,050.8,42.4M,-03.06,+11.64,-01.84;')
    DataPoint(timestamp=time.struct_time(tm_year=2015, tm_mon=10, tm_mday=8, tm_hour=18, tm_min=36, tm_sec=3, tm_wday=3, tm_yday=281, tm_isdst=-1), lat=37.743476666666666, lon=-122.40619999999998, speed=50.8)
    """
    items = line.strip(';').split(',')
    if len(items) != len(GpsLogEntry._fields):
        return None
    parsed = GpsLogEntry(*items)
    timestamp = time.strptime(parsed.date + parsed.time, '%d%m%y%H%M%S.000')
    if parsed.lat == '0000.0000' or parsed.lon == '0000.0000':
        return None
    lat = DmmToD(float(parsed.lat), parsed.lat_dir == 'S')
    lon = DmmToD(float(parsed.lon), parsed.lon_dir == 'W')
    return DataPoint(timestamp=timestamp, lat=lat, lon=lon, speed=float(parsed.speed))


def ParseFile(fn):
    logging.info('Parsing %s', fn)
    out = []
    with open(fn) as fh:
        for line in fh:
            parsed = ParseLine(line)
            if parsed:
                out.append(parsed)
    return out


def IsGpsLogFile(filename):
    return filename.startswith('gps') and filename.endswith('.log')


def ParseLogs(root):
    if os.path.isfile(root):
        return ParseFile(root)
    out = []
    for dir_path, _, filenames in os.walk(root):
        for filename in filenames:
            if IsGpsLogFile(filename):
                full_path = os.path.join(dir_path, filename)
                out.extend(ParseFile(full_path))
    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod()
