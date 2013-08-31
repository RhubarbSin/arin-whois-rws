#!/usr/bin/env python

# rdns NAME
# ip ADDRESS
# cidr ADDRESS

import argparse

class Parser(argparse.ArgumentParser):

    org = None

    def __init__(self, *args, **kwargs):
        super(Parser, self).__init__(*args, **kwargs)

    def populate(self):
        self.add_argument('--output', choices=('xml', 'text', 'html'),
                          default='text')
        self.subparsers = self.add_subparsers(title='Commands', metavar='',
                                              dest='command')
        self._add_org()

    def _add_org(self):
        self.org = self.subparsers.add_parser('org', help='--handle HANDLE --name NAME --dba DBA')
        self.org.add_argument('--handle', help='Org handle')
        self.org.add_argument('--name', help='Org name')
        self.org.add_argument('--dba', help='Org DBA')

class WhoisRwsError(Exception):

    def __init__(self, *args):
        super(WhoisRwsError, self).__init__(*args)

class RestfulCall(object):

    parser = None
    required = None

    def __init__(self, args):
        self.args = args
        error_if_missing(self.parser, args, self.required)
        self.parser.set_defaults(func=self.call)

    def call(self):
        print self.args

class Org(RestfulCall):

    parser = Parser.org
    required = ('handle', 'name', 'dba')

    def __init__(self, args):
        super(Org, self).__init__(args)

def error_if_missing(parser, args, required):
    """Call parser's error method if all attributes specified by
    required are None in args Namespace.
    """

    if not any([getattr(args, arg) for arg in required]):
        parser.error('Missing argument')

def org(args):
    error_if_missing(parser_org, args, ('handle', 'name', 'dba'))
    print args

def customer(args):
    error_if_missing(parser_org, args, ('handle', 'name'))
    print args

def net(args):
    error_if_missing(parser_org, args, ('handle', 'name'))
    print args

def cidr(args):
    print args.cidr

# parser_customer = subparsers.add_parser('customer', help='--handle HANDLE --name NAME')
# parser_customer.add_argument('--handle')
# parser_customer.add_argument('--name')
# parser_customer.set_defaults(func=customer)

# parser_net = subparsers.add_parser('net', help='--handle HANDLE --name NAME')
# parser_net.add_argument('--handle')
# parser_net.add_argument('--name')
# parser_net.set_defaults(func=net)

# parser_cidr = subparsers.add_parser('cidr', help='CIDR')
# parser_cidr.add_argument('cidr', metavar='CIDR')
# parser_cidr.set_defaults(func=cidr)

if __name__ == '__main__':
    p = Parser()
    p.populate()
    args = p.parse_args()
    if args.command == 'org':
        
