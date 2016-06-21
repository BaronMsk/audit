from django import forms
from models import Host
import re


class HostF(forms.Form):
    hostname = forms.CharField(label='hostname', max_length=100)
    ipaddress = forms.CharField(label='ipaddress', max_length=15)
    hosttype = forms.CharField(label='hosttype', max_length=15)
    hoststatus = forms.CharField(label='hoststatus', max_length=15)

    def clean_hostname(self):
        hostname = self.cleaned_data['hostname']
        p = re.compile('\w*')
        if hostname is not None and p.match(hostname):
            return hostname
        else:
            raise forms.ValidationError(u'host name is blank', code=12)

    def clean_ipaddress(self):
        ipaddress = self.cleaned_data['ipaddress']
        p = re.compile('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
        if ipaddress is not None and p.match(ipaddress):
            return ipaddress
        else:
            raise forms.ValidationError(u'ip address is blank', code=12)
    def clean_hosttype(self):
        hosttype = self.cleaned_data['hosttype']
        p = re.compile('(^FreeBSD$|^Linux$)')
        if hosttype is not None and p.match(hosttype):
            return hosttype
        else:
            raise forms.ValidationError(u'host type is not valid', code=12)

    def clean_hoststatus(self):
        hoststatus = self.cleaned_data['hoststatus']
        p = re.compile('(^enabled$|^desabled$)')
        if hoststatus is not None and p.match(hoststatus):
            return hoststatus
        else:
            raise forms.ValidationError(u'host status is not valid', code=12)

    def save(self):
        hostname = self.clean_hostname()
        ipaddress = self.clean_ipaddress()
        hosttype = self.clean_hosttype()
        hoststatus = self.clean_hoststatus()
        f = Host.objects.create(host_name=hostname, host_address=ipaddress, host_type=hosttype, host_status=hoststatus)