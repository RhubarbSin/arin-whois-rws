import requests

import payload
from payload import org

BASE_URL = 'http://whois.arin.net/rest/'

class Caller(object):

    def __init__(self, args):
        if args.call == 'org':
            call = Org
        elif args.call == 'orgs':
            call = Orgs
        self.call = call(**vars(args))

    def run(self):
        return self.call.run()

class Call(object):

    resource = None  # WHOIS-RWS resource name for URL
    params = ()  # sequence of WHOIS-RWS matrix parameters

    def __init__(self, **kwargs):
        self.url = BASE_URL + self.resource

    def run(self):
        print self.url
        response = requests.get(self.url)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        print response.content
        return self.module.parseString(response.content)

class SimpleCall(Call):

    """Class for individual resources.

    Calls look like /RESOURCE/HANDLE.
    """

    def __init__(self, **kwargs):
        super(SimpleCall, self).__init__(**kwargs)
        self.url += '/' + kwargs['handle']

class UnrelatedCall(Call):


    """Class for lists of unrelated resources.

    Calls look like /RESOURCE;param=value.
    """

    def __init__(self, **kwargs):
        super(UnrelatedCall, self).__init__(**kwargs)
        for param in self.params:
            if kwargs[param]:
                self.url += ';%s=%s' % (param, kwargs[param])

class RelatedCall(Call):

    """Class for resources related to resources.

    Calls look like /RESOURCE/HANDLE/RESOURCES.
    """

    pass

class Org(SimpleCall):

    resource = 'org'
    module = payload.org
            
class Orgs(UnrelatedCall):

    resource = 'orgs'
    params = ('handle', 'name', 'dba')
