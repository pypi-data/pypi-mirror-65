#!/usr/bin/env python3

import sys, os, re, arrow, time, pytz
from datetime import datetime
from dateutil import tz

gmt = tz.gettz('UTC')
ltz = tz.gettz('AEST')

dts = [
	'YYYY-MM-DD HH:mm:ss',
	'YYYY-MM-DD',
]


def to_re(dts):
	for token in 'YMDHms':
		dts = dts.replace(token, '\d')
	dts = dts.replace('/', '\-')
	dts = dts.replace(':', '\.')
	return re.compile('.*(%s).*' % dts)


dts_p = list(map(to_re, dts))

for file in os.listdir('.'):
	if not file.lower().endswith('.pdf'):
		continue

	sys.stdout.write(file)

	for p in dts_p:
		m = p.match(file)
		if m:
			dts_v = m.group(1)
			dts_v = dts_v.replace('/', '-')
			dts_v = dts_v.replace('.', ':')
			at = arrow.get(dts_v)
			nt = at.naive.replace(tzinfo=ltz)
			ut = time.mktime(nt.timetuple())
			if ut != os.stat(file).st_mtime:
				os.utime(file, (ut, ut))
				sys.stdout.write(' -> %s' % nt.astimezone(ltz))

			break

	sys.stdout.write('\n')

