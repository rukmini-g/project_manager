from django.contrib.auth import authenticate, login
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages


def login_user(request):
    username = password = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.POST.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect('/ticket/dashboard/')
        else:
            messages.warning(
                request, "Please enter valid username or password")
            return HttpResponseRedirect("/")

    return render_to_response(
        'signin.html',
        {'username': username},
        context_instance=RequestContext(request))