from django import forms
from models import Host
import re


class HostF(forms.Form):
    hostname = forms.CharField(label='hostname', max_length=100)
    ipaddress = forms.CharField(label='ipaddress', max_length=15)

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

    def save(self):
        hostname = self.clean_hostname()
        ipaddress = self.clean_ipaddress()
        f = Host.objects.create(host_name=hostname, host_address=ipaddress)