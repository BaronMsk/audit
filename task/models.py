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
        return u"%s %s %s %s %s %s" % self.host_name, self.host_address, self.host_type, self.host_status, self.host_data_create, self.pk

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
            HostDetails.objects.create(detail_content='test', detail_host_id='%s' % id)
            return True
        except:
            return False

class HostDetails(models.Model):
    detail_content = models.TextField(max_length=65000)
    detail_host_id = models.TextField(max_length=20)
    detail_date_audit = models.DateField(auto_now=True)
    def __unicode__(self):
        return u"%s %s" % self.detail_data_audit, self.detail_content




