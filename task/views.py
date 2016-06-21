from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from task.models import Host, HostDetails, Vulnerability
from django.template import Context, loader
from task.forms import HostF

def index(request):
    host_list = Host.objects.order_by('-host_name')[:100]
    template = loader.get_template('index.html')
    context = Context({
        'host_list': host_list,

    })
    return HttpResponse(template.render(context))

def delete_host(request, id):
    d = Host().dell(id)
    if d == True:
        return HttpResponseRedirect('../')
    else:
        return HttpResponseRedirect('./error/')

def play_host(request, id):
    d = Host().play(id)
    if d == True:
        return HttpResponseRedirect('../')
    else:
        return HttpResponseRedirect('./error/')


def host(request,*args, **kwargs):
    id = args
    details_list = Vulnerability.objects.filter(host_id='%s' % id)
    template = loader.get_template('details.html')
    context = Context({
        'details_list': details_list,
    })
    return HttpResponse(template.render(context))


def create_host(request):
    return render(request,'host.html')


def host_add(request):
    if request.method == 'POST':
        form = HostF(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../')
        else:
            return HttpResponse('no valid')
    else:
        form = HostF()
    return render(request, 'host.html', {'hostname': form})