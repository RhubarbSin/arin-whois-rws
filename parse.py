import argparse

class ParserResource(object):

    def __init__(self, command, positional=None, *options):
        self.command = command
        self.positional = positional
        self.option = dict((option[0], option[1]) for option in options)

    @property
    def help_(self):
        h = self.positional[0].upper() if self.positional else ''
        for name in self.option:
            h += (' --%s %s' % (name, name.upper()))
        return h

class Parser(argparse.ArgumentParser):

    resources = (ParserResource('poc', ('handle', 'the handle of the POC')),
                 ParserResource('org', ('handle', 'the handle of the organization')),
                 ParserResource('net', ('handle', 'the handle of the network')),
                 ParserResource('asn', ('handle', 'the handle of the ASN')),
                 ParserResource('customer', ('handle', 'the handle of the customer')),
                 ParserResource('rdns', ('name', 'the name of the delegation (e.g. 0.192.in-addr.arpa.)')),

                 ParserResource('orgs', None,
                                ('handle', 'the handle of the organization'),
                                ('name', 'the name of organization'),
                                ('dba', 'the name the organization does business as')),
                 ParserResource('customers', None,
                                ('handle', 'the handle of the customer'),
                                ('name', 'the name of the customer')),
                 ParserResource('pocs', None,
                                ('handle', 'the handle of the POC'),
                                ('domain', 'the domain of the email address for the POC'),
                                ('first', 'the first name of the POC'),
                                ('last', 'the last name of the POC'),
                                ('company', 'the company name registered by the POC'),
                                ('city', 'the city registered by the POC')),
                 ParserResource('asns', None,
                                ('handle', 'the handle of the ASN'),
                                ('name', 'the name of the ASN')),
                 ParserResource('nets', None,
                                ('handle', 'the handle of the network'),
                                ('name', 'the name of the network')),
                 ParserResource('rdns', None,
                                ('name', 'the name of the delegation (e.g. 0.192.in-addr.arpa.)')))



    def populate(self):
        self.add_argument('--output', choices=('xml', 'text', 'html'),
                          default='text')
        subparsers = self.add_subparsers(title='Commands', metavar='',
                                         dest='call')
        for resource in self.resources:
            self._add_subparser(subparsers, resource)

    def run(self):
        return self.parse_args()

    def _add_subparser(self, subparsers, resource):
        subparser = subparsers.add_parser(resource.command,
                                          help=resource.help_)
        if resource.positional:
            subparser.add_argument(resource.positional[0],
                                   metavar=resource.positional[0].upper(),
                                   help=resource.positional[1])
        for name, description in resource.option.iteritems():
            subparser.add_argument('--%s' % name, metavar=name.upper(),
                                   help=description)

    def _add_org_related(self, subparsers):
        subparser = subparsers.add_parser('org-related', help='--handle HANDLE --resource RESOURCE')
        subparser.add_argument('--handle', help='Org handle')
        subparser.add_argument('--resource', help='Resource')
