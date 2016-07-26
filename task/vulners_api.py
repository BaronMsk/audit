import json, urllib


class VulnersApi(object):
    def get_vulners_info(self, id):
        url = "http://vulners.com/api/v3/search/id/?id=" + id
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        not_found_cve = data['data']['documents']
        try:
            score = data['data']['documents']['cvss']['score']
            description = data['data']['documents']['description']
        except KeyError:
            score = 'Not found'
            description = 'Not found'
            return description, score
        return description, score
