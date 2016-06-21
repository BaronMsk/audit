from __future__ import unicode_literals
from django.db import models
from get_port_audit import *


# Create your models here.

class Host(models.Model):
    host_name = models.CharField(max_length=255)
    host_address = models.TextField(max_length=20)
    host_type = models.TextField(max_length=20)
    host_data_create = models.DateField(auto_now=True)
    host_status = models.TextField(max_length=20)

    def __unicode__(self):
        return self.host_address

    def get_absolute_url(self):
        return '/host/%d' % self.pk

    def dell(self, id):
        try:
            Host.objects.filter(pk='%s' % id).delete()
            HostDetails.objects.filter(detail_host_id='%s' % id).delete()
            return True
        except:
            return False

    def play(self, id):
        try:
            Vulnerability.objects.filter(host_id='%s' % id).delete()
            ip = Host.objects.filter(pk='%s' % id).values('host_address')
            ip = ip[0]['host_address']
            data = get_info_freebsd(ip)
            data = data.split('\n\n')
            for i in data:
                result = get_prog(i)
                if result == None:
                    continue
                else:
                    programm_d = result[0]
                    www_d = result[1]
                    cve_d = result[2][0:]
                    cve_d = ', '.join(cve_d)
                    Vulnerability.objects.create(programm=programm_d, url=www_d, host_id=id, cve_list=cve_d)
            return True
        except:
            return False

class HostDetails(models.Model):
    detail_content = models.TextField(max_length=65000)
    detail_host_id = models.TextField(max_length=20)
    detail_date_audit = models.DateField(auto_now=True)
    def __unicode__(self):
        return u"%s %s" % self.detail_data_audit, self.detail_content


class Vulnerability(models.Model):
    programm = models.TextField(max_length=1000)
    url = models.TextField(max_length=1000)
    host_id = models.ImageField()
    cve_list = models.TextField(max_length=65000, blank=True)
