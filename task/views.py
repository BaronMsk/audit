from django.shortcuts import render
from django.http import HttpResponse
from task.models import Host, HostDetails
from django.template import Context, loader

# Create your views here.


def index(request):
    host_list = Host.objects.order_by('-host_name')[:10]
    template = loader.get_template('task/index.html')
    context = Context({
        'host_list': host_list,

    })
    return HttpResponse(template.render(context))

def host(request,*args, **kwargs):
    id = args
    details_list = HostDetails.objects.filter(detail_host_id='%s' % id)[:10]
    template = loader.get_template('task/details.html')
    context = Context({
        'details_list': details_list,
    })
    return HttpResponse(template.render(context))


def create_host(request):
    template = loader.get_template('task/host.html')
    context = Context({

    })
    return HttpResponse(template.render(context))