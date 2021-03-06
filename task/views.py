from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from task.models import Host, Vulnerability
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
    d = Host().delete(id)
    if d == True:
        return HttpResponseRedirect('../')
    else:
        return HttpResponseRedirect('./error/')

def play_host(request, id):
    status_task = Host().play(id)
    template = loader.get_template('error.html')
    context = Context({
        'status_task': status_task,
    })
    if status_task == True:
        host_url = '/host/' + id
        return HttpResponseRedirect(host_url)
    elif status_task == u"NotKeyPassword":
        return HttpResponse(template.render(context))
    elif status_task == u'BadAuthentication':
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('./error/')


def host(request, *args):
    id = args
    details_list = Vulnerability().detail_content(id)
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


def score(request, *args):
    id = args
    d = Vulnerability().get_all_cve(id)
    result_vul = []
    for i in d:
        result_vul += [Vulnerability().get_all_vulnerability(i)]
    host_info = Vulnerability().get_host_info(id)
    template = loader.get_template('score.html')
    context = Context({
        'result_vul': result_vul,
        'host_info': host_info,

    })
    return HttpResponse(template.render(context))


def dashboard(request, *args):
    dash_result = []
    template = loader.get_template('dashboard.html')
    host_list = Host.objects.filter().values('id')
    for i in host_list:
        id = i['id']
        dash_result += [Vulnerability().get_dash_info(id)]
    context = Context({
        'dash_result': dash_result,
    })
    return HttpResponse(template.render(context))


def key(request, *args):
    template = loader.get_template('key.html')
    return HttpResponse(template.render())
