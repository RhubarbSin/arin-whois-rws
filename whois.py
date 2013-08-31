#!/usr/bin/env python

import parse
import call

parser = parse.Parser()
parser.populate()
args = parser.run()
caller = call.Caller(args)
output = caller.run()
