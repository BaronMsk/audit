import paramiko
import re


def get_info_freebsd(host):
    USER = 'zhukov'
    KEY = '/home/baron/.ssh/id_rsa'
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=USER, key_filename=KEY)
        stdin, stdout, stderr = client.exec_command('pkg audit')
        data = stdout.read() + stderr.read()
        report = "%s" % (data)
        client.close()
        return report
    except:
        return host + 'Error connect'


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



#data = get_info_freebsd('10.1.12.120')


#data = data.split('\n\n')

#for i in data:
#    result = get_prog(i)
#    if result == None:
#        continue
#    else:
#        print result
