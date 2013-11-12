#!/usr/bin/python

from cookielib import CookieJar
import urllib
import urllib2
import sys
import json
import codecs

logonparams = {
    'action': 'login',
    'lgname': sys.argv[2],
    'lgpassword': sys.argv[3],
    'format': 'json'
}

pageparams = {
    'action': 'parse',
    'format': 'json',
    'page': sys.argv[1],
    'prop': 'text|images|displaytitle|headitems|headhtml',
    'contentmodel': 'text'
}

user_agent = 'BookExtractorScript (mwalker@wikimedia.org)'

logonurl = "https://en.wikipedia.org/w/api.php"
pageurl = "https://en.wikipedia.org/w/api.php"

headers = { 'User-Agent' : user_agent }

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# First logon request
req = urllib2.Request(logonurl, urllib.urlencode(logonparams), headers)
response = opener.open(req)

data = json.loads(response.read())
token = data['login']['token']
logonparams['lgtoken'] = token

if data['login']['result'] != "NeedToken":
    print("ERROR -- did not get expected result from server whilst logging in")
    exit(1)

# Second logon request
req = urllib2.Request(logonurl, urllib.urlencode(logonparams), headers)
response = opener.open(req)

data = json.loads(response.read())
if data['login']['result'] != 'Success':
    print("ERROR -- login was not successful! invalid username/password?")
    exit(1)

# page request
req = urllib2.Request(pageurl, urllib.urlencode(pageparams), headers)
response = opener.open(req)

data = json.loads(response.read())
# keys here are ['parse'] -> [u'headitems', u'displaytitle', u'title', u'text', u'headhtml', u'images']

of = codecs.open('out.html', 'w', 'utf-8')
of.write(data['parse']['text']['*'])
of.flush()
of.close()

of = codecs.open('headitems.html', 'w', 'utf-8')
of.write(data['parse']['headitems'][0])
of.flush()
of.close()

of = codecs.open('headhtml.html', 'w', 'utf-8')
of.write(data['parse']['headhtml']['*'])
of.flush()
of.close()
