#! /usr/bin/env python

"""Dump the list of tracked windows to standard error.

This illustrates a very simple example of using get_windowlist()
"""

import sys
import Fvwm


def cmp_window_names(w1, w2):
    return cmp(w1.name, w2.name)


def dump_window_list(wlist):
    # wlist is an instance of the Tracker.Tracker class
    print 'Number of windows:', wlist.window_count()
    # allwindows is a list of all window names
    allwindows = wlist.get_windows()
    # sort the windows alphabetically, using the above function
    allwindows.sort(cmp_window_names)
    # one window on each screen has no name. use something better
    for window in allwindows:
        if not window.name:
            window.name = '<unnamed>'
    # now print out all the window names and their origins
    for window in allwindows:
        print '    %s is at [%d, %d]' % (
            window.name, window.x, window.y)


if __name__ == '__main__':
    # pass the script arguments to the interface class
    m = Fvwm.FvwmModule(sys.argv)
    # get the window list
    wlist = m.get_windowlist()
    # set up the `print' statement so that all output goes to standard error.
    # First, retain the old standard out
    stdout = sys.stdout
    try:
        # now set the new standard out to point to standard error
        sys.stdout = sys.stderr
        dump_window_list(wlist)
    finally:
        # always restore standard out
        sys.stdout = stdout
