from django import forms
import datetime

class HostF(forms.Form):
    hostname = forms.CharField(label='hostname', max_length=100)
    ipaddress = forms.CharField(label='ipaddress', max_length=15)
    date_create = forms.DateField(initial=datetime.date.today)