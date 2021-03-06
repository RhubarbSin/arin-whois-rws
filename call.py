import requests

import payload
from payload import poc, org, network, orgList

BASE_URL = 'http://whois.arin.net/rest/'

class Call(object):

    """Base class for ARIN Whois-RWS call."""

    resource = None  # Whois-RWS resource name for URL
    module = None  # generateDS module for returned payload
    params = ()  # sequence of Whois-RWS matrix parameters

    def __init__(self, **kwargs):
        self.url = BASE_URL + self.resource

    def run(self):
        response = requests.get(self.url)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        print response.content
        return self.module.parseString(response.content)

class IndividualCall(Call):

    """Class for individual resources calls.

    Calls look like /RESOURCE/HANDLE.
    """

    def __init__(self, **kwargs):
        super(IndividualCall, self).__init__(**kwargs)
        self.url += '/' + kwargs['handle']

class UnrelatedCall(Call):

    """Class for lists of unrelated resources.

    Calls look like /RESOURCES;PARAM=VALUE.
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

class Poc(IndividualCall):

    resource = 'poc'
    module = payload.poc

class Org(IndividualCall):

    resource = 'org'
    module = payload.org

class Net(IndividualCall):

    resource = 'net'
    module = payload.network
            
class Orgs(UnrelatedCall):

    resource = 'orgs'
    module = payload.orgList
    params = ('handle', 'name', 'dba')

class Caller(object):

    """Class for method object that uses Call subclasses."""

    callmap = {'org': Org,
               'poc': Poc,
               'net': Net,
               'orgs': Orgs}

    def __init__(self, args):
        """Instantiate appropriate Call subclass for command in args."""

        call = self.callmap[args.command]  # get corresponding class name
        self.call = call(**vars(args))  # instantiate class with dict

    def run(self):
        return self.call.run()
