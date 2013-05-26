import dbm
import urllib2
import lxml.html

def fetch_nocache(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Infobox fetcher (+infoboxfetch@zielm.com)')
    opener = urllib2.build_opener()
    opener.addheaders = []
    data = opener.open(url).read()
    return data

def stringify_children(node):
    return (node.text or '')\
        + ''.join( stringify_children(child) + (child.tail or '') for child in node.getchildren() )

def fetch_html(url):
    if '://' not in url:
        url = 'http://en.wikipedia.org/wiki/%s' % url
    cache = dbm.open('cache', 'c')
    if url not in cache:
        cache[url] = fetch_nocache(url)
    return lxml.html.fromstring(cache[url])
