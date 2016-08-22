import paramiko
import re
import traceback
import logging
import json
import urllib2
from django.db import connection
from django.conf import settings

USER = getattr(settings, 'SSH_USER', None)
KEY = getattr(settings, 'SSH_KEY', None)


VULNERS_LINKS = {'pkgChecker': 'https://vulners.com/api/v3/audit/audit/',
                 'bulletin': 'https://vulners.com/api/v3/search/id/?id=%s&references=True'}

def get_rsa_password():
    cursor = connection.cursor()
    sql = """SELECT id_rsa_pass FROM id_rsa"""
    cursor.execute(sql)
    data = cursor.fetchone()
    return data

def get_info_host(host, type):
    KeyPassword = get_rsa_password()
    if not KeyPassword:
        return u'NotKeyPassword'
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=USER, key_filename=KEY, password=KeyPassword[0])
        if type == u'FreeBSD':
            stdin, stdout, stderr = client.exec_command('pkg audit')
        elif type == u'Linux':
            stdin, stdout, stderr = client.exec_command("dpkg-query -W -f='${Package} ${Version} ${Architecture}\n'")
        data = stdout.read() + stderr.read()
        report = "%s" % (data)
        client.close()
        return report
    except paramiko.ssh_exception.SSHException as (errno, strerror):
        return host + 'SSH Connect Error [' + errno + ']: "' + strerror + '"'
    except Exception as e:
        logging.error(traceback.format_exc())
        # Logs the error appropriately.


def get_prog(data):
    datas = data.split('\n')
    cve = []
    for i in datas:
        try:
            found = re.search(r'is vulnerable:', i)
            if found:
                programm = i.split()[0]
            found = re.search(r'^WWW:', i)
            if found:
                www = i.split()[1]
            found = re.search(r'^CVE:', i)
            if found:
                cve += [i.split()[1]]
            return programm, www, cve
        except:
            continue


# __author__ = 'isox'
def auditSystem(data):
    dsa = u'NotFoundVulDpkg'
    installedPackages = data
    # Get vulnerability information
    payload = {'os':'debian',
               'version':'8',
               'package':installedPackages}
    req = urllib2.Request(VULNERS_LINKS.get('pkgChecker'))
    req.add_header('Content-Type', 'application/json')
    binary_data = (json.dumps(payload)).encode('utf8')
    response = urllib2.urlopen(req, binary_data)
    responseData = response.read()
    if isinstance(responseData, bytes):
        responseData = responseData.decode('utf8')
    responseData = json.loads(responseData)
    dsa = (responseData.get('data').get('vulnerabilities'))
    return dsa

