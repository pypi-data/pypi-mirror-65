import json
from .py_version import PY2

if PY2:
    from urllib2 import urlopen, Request  # pylint: disable=E0401 # pytype: disable=import-error
else:
    from urllib.request import urlopen, Request


class Response:
    def __init__(self, headers, body):
        self.headers = headers
        self.body = body

        self.Authorized = self.body["Authorized"]
        # pricing plans are: Hobby, Pro, Enterprise
        self.PricingPlan = self.body["PricingPlan"]


class Http:
    def __init__(self, url, data=None, headers={}, timeout=2.376):
        self.url = url
        self.data = data
        self.headers = headers
        # self.method = method
        # python2 does not have method arg; https://sourcegraph.com/github.com/python/cpython@2.7/-/blob/Lib/urllib2.py#L226
        self.timeout = timeout
        self.encoding = "utf8"

        # https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b310-urllib-urlopen
        if not self.url.lower().startswith("http"):
            raise ValueError("`url` should be a http:// or https:// scheme")

    def request(self):
        # In python2, the Request class does not take a method argument
        # whereas it can in python3
        # see; https://sourcegraph.com/github.com/python/cpython@2.7/-/blob/Lib/urllib2.py#L226
        req = Request(url=self.url, data=self.data, headers=self.headers)
        f = urlopen(  # nosec, security vulnerability fixed in __init__ method
            req, timeout=self.timeout
        )
        headers = f.info().items()
        body = f.read()
        f.close()

        headers = self._headers_as_dict(headers)
        assert isinstance(headers, dict)

        if isinstance(body, bytes) and not PY2:
            body = body.decode(self.encoding)
        assert isinstance(body, str)

        return Response(headers=headers, body=json.loads(body))

    def req_n_auth(self,):
        """
        We give people the benefit of doubt.
        We only consider people to be not authorized if the
        backend comes back with an authoritative answer to that effect.

        Else, any errors or any other outcome; we assume authorization is there
        and also assume they belong to the highest pricing plan: Enterprise
        """
        try:
            resp = self.request()
            return resp.Authorized, resp.PricingPlan
        except Exception:
            # failure of errorship should not lead to people been unable
            # to ship exceptions
            return True, "Enterprise"

    @staticmethod
    def _headers_as_dict(lst):
        """
        lst is a list of tuples like;
            [('Date', 'Tue, 10 Dec 2019 09:06:16 GMT'), ('Expires', '-1')]
        """
        x = {}
        for i in lst:
            x[i[0]] = i[1]

        return x
