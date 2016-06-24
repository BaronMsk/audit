from __future__ import unicode_literals
from django.db import models
from get_port_audit import *
from vulners_api import *


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

    def delete(self, id):
        try:
            Host.objects.filter(pk='%s' % id).delete()
            Vulnerability.objects.filter(host_id='%s' % id).delete()
            return True
        except:
            return False

    def get_info_vulners(self, id):
        found_cve_todb = Vulnerability.objects.filter(host_id='%s' % id).values('cve_list')
        if found_cve_todb:  # found cve
            for f in found_cve_todb:
                cve_list = f['cve_list']
                cve_list = cve_list.split(',')
                for i in cve_list:
                    found_cve_todb = CVEdetails.objects.filter(cve='%s' % i).values('cve')
                    if not found_cve_todb:  # if not found then create to db
                        va = VulnersApi()
                        result = va.get_vulners_info(i)
                        description_d = result[0]
                        score_d = result[1]
                        if description_d == 'Not found':
                            continue
                        CVEdetails.objects.create(cve=i, description=description_d, score=score_d)
                    else:
                        result = CVEdetails.objects.filter(cve=i).values()


        else:
            ##if id host not found
            return None


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
                    cve_d = ','.join(cve_d)
                    Vulnerability.objects.create(programm=programm_d, url=www_d, host_id=id, cve_list=cve_d)
            return True
        except:
            return False


class Vulnerability(models.Model):
    programm = models.TextField(max_length=1000)
    url = models.TextField(max_length=1000)
    host_id = models.ImageField()
    cve_list = models.TextField(max_length=65000, blank=True)

    def detail_content(self, id):
        details_list = Vulnerability.objects.filter(host_id='%s' % id)
        details_list = details_list.distinct()
        return details_list

    def get_all_cve(self, id):
        all_cve_list = []
        all_cve = Vulnerability.objects.filter(host_id='%s' % id).values('cve_list')
        for i in all_cve:
            all_cve_list += [i['cve_list']]
        return all_cve_list

    def get_all_vulnerability(self, cve_id):
        all_vulnerability = []
        for i in cve_id.split(','):
            all_vulnerability = CVEdetails.objects.filter(cve=i).values('description', 'score', 'cve')
            return all_vulnerability

class CVEdetails(models.Model):
    cve = models.TextField(max_length=65000)
    description = models.TextField(max_length=65000)
    score = models.DecimalField(max_digits=5, decimal_places=1)
