import argparse

class ParserResource(object):

    def __init__(self, command, positional={}, optional={}):
        self.command = command
        self.positional = positional
        self.optional = optional

    @property
    def help_(self):
        h = ''
        for name in self.positional:
            h += ' %s' % name.upper()
        for name in self.optional:
            h += (' --%s %s' % (name, name.upper()))
        return h

class Parser(argparse.ArgumentParser):

    resources = (ParserResource('poc', {'handle': 'the handle of the POC'}),
                 ParserResource('org', {'handle': 'the handle of the organization'}),
                 ParserResource('net', {'handle': 'the handle of the network'}),
                 ParserResource('asn', {'handle': 'the handle of the ASN'}),
                 ParserResource('customer', {'handle': 'the handle of the customer'}),
                 ParserResource('rdns', {'name': 'the name of the delegation (e.g. 0.192.in-addr.arpa.)'}),

                 ParserResource('orgs',
                                optional={'handle': 'the handle of the organization',
                                          'name': 'the name of organization',
                                          'dba': 'the name the organization does business as'}),
                 ParserResource('customers',
                                optional={'handle': 'the handle of the customer',
                                          'name': 'the name of the customer'}),
                 ParserResource('pocs',
                                optional={'handle': 'the handle of the POC',
                                          'domain': 'the domain of the email address for the POC',
                                          'first': 'the first name of the POC',
                                          'last': 'the last name of the POC',
                                          'company': 'the company name registered by the POC',
                                          'city': 'the city registered by the POC'}),
                 ParserResource('asns',
                                optional={'handle': 'the handle of the ASN',
                                          'name': 'the name of the ASN'}),
                 ParserResource('nets',
                                optional={'handle': 'the handle of the network',
                                          'name': 'the name of the network'}),
                 ParserResource('rdns',
                                optional={'name': 'the name of the delegation (e.g. 0.192.in-addr.arpa.)'}),
                 ParserResource('pocs-related',
                                optional={'handle': 'the handle of the POC',
                                          'resource': 'the type of resource associated with the POC'}))

    def populate(self):
        self.add_argument('--output', choices=('xml', 'text', 'html'),
                          default='text')
        subparsers = self.add_subparsers(title='Commands', metavar='',
                                         dest='command')
        for resource in self.resources:
            self._add_subparser(subparsers, resource)

    def run(self):
        return self.parse_args()

    def _add_subparser(self, subparsers, resource):
        subparser = subparsers.add_parser(resource.command,
                                          help=resource.help_)
        for name, description in resource.positional.iteritems():
            subparser.add_argument(name, metavar=name.upper(),
                                   help=description)
        for name, description in resource.optional.iteritems():
            subparser.add_argument('--%s' % name, metavar=name.upper(),
                                   help=description)

    def _add_org_related(self, subparsers):
        subparser = subparsers.add_parser('org-related', help='--handle HANDLE --resource RESOURCE')
        subparser.add_argument('--handle', help='Org handle')
        subparser.add_argument('--resource', help='Resource')
