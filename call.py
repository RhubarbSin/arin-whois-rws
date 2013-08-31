import requests

BASE_URL = 'http://whois.arin.net/rest/'

class Caller(object):

    def __init__(self, args):
        if args.call == 'orgs':
            call = Orgs
        self.call = call(**vars(args))

    def run(self):
        return self.call.run()

class Call(object):

    resource = None  # WHOIS-RWS resource name for URL
    params = ()  # sequence of WHOIS-RWS matrix parameters

    def __init__(self, **kwargs):
        self.url = BASE_URL + self.resource
        for param in self.params:
            if kwargs[param]:
                self.url += ';%s=%s' % (param, kwargs[param])

    def run(self):
        print self.url
        response = requests.get(self.url)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        print response.content

class Org(Call):

    resource = 'org'

    def __init__(self, **kwargs):
        pass
            
class Orgs(Call):

    resource = 'orgs'
    params = ('handle', 'name', 'dba')
