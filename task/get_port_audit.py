import paramiko


def get_info_freebsd(host):
    USER = 'zhukov'
    KEY = '/home/baron/.ssh/id_rsa'
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=USER, key_filename=KEY)
        stdin, stdout, stderr = client.exec_command('pkg audit')
        data = stdout.read() + stderr.read()
        report = "\r%s%s \r" % (host, data)
        client.close()
        return report
    except:
        return host + 'Error connect'
