#!/usr/bin/python
# Convert iCalendar data to plaintext (very basic, don't rely on it :)
# Requirements: python-vobject (http://vobject.skyhouseconsulting.com/)
# This file is part of urlwatch
#
# Copyright (c) 2008-2011 Thomas Perl <thp.io/about>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


def ical2text(ical_string):

    try:
        import vobject
    except ImportError:
        sys.stderr.write("vobject not installed. Ubuntu/Debian: sudo apt-get install python-vobject")
        sys.exit(2)

    result = []
    if isinstance(ical_string, unicode):
        parsedCal = vobject.readOne(ical_string)
    else:
        try:
            parsedCal = vobject.readOne(ical_string)
        except:
            parsedCal = vobject.readOne(ical_string.decode('utf-8', 'ignore'))

    for event in parsedCal.getChildren():
        if event.name == 'VEVENT':
            if hasattr(event, 'dtstart'):
                start = event.dtstart.value.strftime('%F %H:%M')
            else:
                start = 'unknown start date'

            if hasattr(event, 'dtend'):
                end = event.dtend.value.strftime('%F %H:%M')
            else:
                end = start

            if start == end:
                date_str = start
            else:
                date_str = '%s -- %s' % (start, end)

            result.append('%s: %s' % (date_str, event.summary.value))

    return '\n'.join(result)


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        print ical2text(open(sys.argv[1]).read())
    else:
        print 'Usage: %s icalendarfile.ics' % (sys.argv[0])
        sys.exit(1)

