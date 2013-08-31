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

    resources = (ParserResource('poc', ('handle', 'POC Handle')),
                 ParserResource('org', ('handle', 'Org handle')),
                 ParserResource('net', ('handle', 'Net handle')),
                 ParserResource('asn', ('handle', 'ASN handle')),
                 ParserResource('customer', ('handle', 'Customer handle')),
                 ParserResource('rdns', ('name', 'Delegation name')),

                 ParserResource('orgs', None,
                                ('handle', 'Org handle'),
                                ('name', 'Org Name'),
                                ('dba', 'Org DBA')))

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

    def _add_orgs(self, subparsers):
        subparser = subparsers.add_parser('orgs', help='--handle HANDLE --name NAME --dba DBA')
        subparser.add_argument('--handle', help='Org handle')
        subparser.add_argument('--name', help='Org name')
        subparser.add_argument('--dba', help='Org DBA')

    def _add_org_related(self, subparsers):
        subparser = subparsers.add_parser('org-related', help='--handle HANDLE --resource RESOURCE')
        subparser.add_argument('--handle', help='Org handle')
        subparser.add_argument('--resource', help='Resource')
