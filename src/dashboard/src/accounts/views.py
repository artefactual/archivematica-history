# This file is part of Archivematica.
#
# Copyright 2010-2012 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
