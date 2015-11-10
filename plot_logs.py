#!/usr/local/bin/python3
#
# Quick hacky script to parse gps logs and plot them on a geolocated bitmap.

import sys
import time

import map
import gps

# Hardcoded coordinates for usa_nw.png.
# WA, tip of olympic peninsula.
PIXEL1 = [115, 131]  # y, x
COORDS1 = [48.358716, -124.722867]
# Denver.
PIXEL2 = [663, 1031]  # y, x
COORDS2 = [39.76453,-105.1353048]


def Plot(log_dir):
    geo = map.GeoLocated(PIXEL1, COORDS1, PIXEL2, COORDS2)

    data = gps.ParseLogs(log_dir)
    data.sort(key=lambda x: x.timestamp)
    prev_date = None
    plotter = None
    for datum in data:
        date = time.strftime('%Y%m%d', datum.timestamp)
        if date != prev_date:
            if plotter:
                plotter.Save('%s.png' % prev_date)
            prev_date = date
            plotter = map.Plotter('usa_nw.png')
            plotter.Text((20, 20), time.strftime('%b %d', datum.timestamp))
        pixel = geo.GetPixel((datum.lat, datum.lon))
        plotter.Square(pixel, 5)
    if plotter:
        plotter.Save('%s.png' % prev_date)


if __name__ == '__main__':

    Plot(sys.argv[1])
