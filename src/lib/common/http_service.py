import urllib
import sys

try:
    from urllib2 import Request, urlopen
except:
    from urllib.request import Request, urlopen

class HttpService():
    def build_url(self, path, **params):
        url = path

        for key, val in params.items():
            if val is not None:
                delimiter = ('?', '&')['?' in url]
                url = url + delimiter + '%s=%s' % (key, urllib.quote(str(val)))

        return url

    def http_request(self, url, headers=None, data=None, method=None):
        if data is not None:
            data = urllib.urlencode(data)
            request = Request(url, data)
        else:
            request = Request(url)

        if method is not None:
            request.get_method = lambda: method

        if headers:
            for key, value in headers.items():
                request.add_header(key, value)

        response = urlopen(request).read()

        if sys.version_info.major == 3:
            response = response.decode('utf-8')

        return response

    def http_request2(self, url, headers=None, data=None, method=None):
        if data is not None:
            data = urllib.urlencode(data)
            request = Request(url, data)
        else:
            request = Request(url)

        if method is not None:
            request.get_method = lambda: method

        if headers:
            for key, value in headers.items():
                request.add_header(key, value)

        response = urlopen(request)

        # if sys.version_info.major == 3:
        #     response = response.decode('utf-8')

        return [response.read(), response]