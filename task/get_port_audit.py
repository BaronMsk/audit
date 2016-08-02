import paramiko
import re
import traceback
import logging
from django.db import connection


def get_rsa_password():
    cursor = connection.cursor()
    sql = """SELECT id_rsa_pass FROM id_rsa"""
    cursor.execute(sql)
    data = cursor.fetchone()
    return data



def get_info_freebsd(host):
    KeyPassword = get_rsa_password()

    if KeyPassword is None:
        return "NotKeyPassword"


    USER = 'zhukov'
    KEY = '/var/www/audit/id_rsa.encrypted.key'
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=USER, key_filename=KEY, password=KeyPassword[0])
        stdin, stdout, stderr = client.exec_command('pkg audit')
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
