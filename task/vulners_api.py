import json, urllib2

__author__ = 'isox'


class VulnersApi(object):
    def getAllCveInfo(self, cve):
        VULNERS_LINKS = {'idResolver': 'https://vulners.com/api/v3/search/id/'}
        payload = {'id': cve}
        req = urllib2.Request(VULNERS_LINKS.get('idResolver'))
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(payload))
        responseData = json.loads(response.read())
        data = (responseData.get('data'))
        return data
