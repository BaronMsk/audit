import json, urllib, urllib2


class VulnersApi(object):
    def get_vulners_info_freebsd(self, id):
        url = "https://vulners.com/api/v3/search/id/?id=" + id
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        if data['result'] == u'OK':
            try:
                score = data['data']['documents'][id]['cvss']['score']
                description = data['data']['documents'][id]['description']
                return description, score
            except:
                return u'NotFound', u'NotFound'
        else:
            return u'APIError', u'APIError'

    def getAllCveInfo(cve):
        VULNERS_LINKS = {'idResolver': 'https://vulners.com/api/v3/search/id/'}
        payload = {'id': cve}
        req = urllib2.Request(VULNERS_LINKS.get('idResolver'))
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(payload))
        responseData = json.loads(response.read())
        return (responseData.get('data'))