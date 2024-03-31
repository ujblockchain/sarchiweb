from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, Context
from csp.decorators import csp_exempt


@csp_exempt
def permission_denied(request, exception):
    return render(request, '403.html', using='django', status=403)


@csp_exempt
def page_not_found(request, exception):
    return render(request, '404.html', using='django', status=404)


@csp_exempt
def server_error(request):
    return render(request, '500.html', using='django', status=500)
