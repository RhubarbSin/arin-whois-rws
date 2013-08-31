#!/usr/bin/env python

from StringIO import StringIO

import parse
import call

parser = parse.Parser()
parser.populate()
args = parser.run()
caller = call.Caller(args)
payload = caller.run()

stringio = StringIO()
payload.export(stringio, 0, namespace_='')
xml = stringio.getvalue()
stringio.close()

import lxml.etree as ET
dom = ET.fromstring(xml)
xslt = ET.parse('website.xsl')
transform = ET.XSLT(xslt)
newdom = transform(dom)
print(ET.tostring(newdom, pretty_print=True))
