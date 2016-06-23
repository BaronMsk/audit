import json, urllib


class VulnersApi(object):
    def get_vulners_info(self, id):
        url = "http://vulners.com/api/v3/search/id/?id=" + id
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        not_found_cve = data['data']['document']
        if not_found_cve == None:
            score = 'Not found'
            description = 'Not found'
            return description, score
        score = data['data']['document']['_source']['cvss']['score']
        description = data['data']['document']['_source']['description']
        return description, score
