import json

try:
    # Python 3
    from urllib.parse import urlparse, urlencode
except ImportError:
    # Python 2
    from urlparse import urlparse
    from urllib import urlencode


def build_url(request):
    if request.body:
        parsed = urlparse(request.url)
        query = '&'.join([parsed.query, urlencode(json.loads(request.body))])
        # return '{parsed.scheme}://{parsed.netloc}{parsed.path}?{query}'
        return '{0:s}://{1:s}{2:s}?{3:s}'.format(
            parsed.scheme, parsed.netloc, parsed.path, query
        )
    return request.url
