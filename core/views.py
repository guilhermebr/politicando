#encoding: utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse

from forms import MailForm
#from django.contrib.auth.forms import AuthenticationForm
import pymongo

from pymongo import Connection

conn = Connection('localhost', 27017)

db = conn.test

emails = db.emails


def home(request):
    context = {}

    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            emails.save({'_id': form.save_mail().encode('ascii')})
            context['success'] = True

    
    return render(request ,'base.html', context)

def quemsomos(request):
    context = {}

#    if request.user.is_authenticated():
#        return redirect('events')
#    else:
#        form = AuthenticationForm()
#        context['form'] = form
    
    return render(request ,'quemsomos.html', context)