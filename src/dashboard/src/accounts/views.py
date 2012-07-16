from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render

@user_passes_test(lambda u: u.is_superuser)
def list(request):
    users = User.objects.all()
    return render(request, 'accounts/list.html', locals())

def edit(request, id=None):
    if id is None:
        user = request.user
    else:
        try:
            user = User.objects.get(pk=id)
        except:
            raise Http404
    return render(request, 'accounts/edit.html', locals())

@user_passes_test(lambda u: u.is_superuser)
def add(request):
    return render(request, 'accounts/add.html', locals())

@user_passes_test(lambda u: u.is_superuser)
def delete(request, id):
    try:
        user = User.objects.get(pk=id)
        if request.user.username == user.username:
            raise Http404
        user.delete()
    except:
        raise Http404
