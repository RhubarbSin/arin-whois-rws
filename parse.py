import argparse

class Parser(argparse.ArgumentParser):

    def populate(self):
        self.add_argument('--output', choices=('xml', 'text', 'html'),
                          default='text')
        subparsers = self.add_subparsers(title='Commands', metavar='',
                                         dest='call')
        self._add_org(subparsers)
        self._add_orgs(subparsers)

    def _add_org(self, subparsers):
        self.org = subparsers.add_parser('org', help='HANDLE')
        self.org.add_argument('handle', metavar='HANDLE', help='Org handle')

    def _add_orgs(self, subparsers):
        self.org = subparsers.add_parser('orgs', help='--handle HANDLE --name NAME --dba DBA')
        self.org.add_argument('--handle', help='Org handle')
        self.org.add_argument('--name', help='Org name')
        self.org.add_argument('--dba', help='Org DBA')

    def run(self):
        return self.parse_args()
