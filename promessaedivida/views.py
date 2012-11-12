#encoding: utf-8

#from django.db.models import Q
#from django.contrib.auth.views import redirect_to_login
#from django.http import HttpResponseRedirect
#from django.contrib.auth.decorators import login_required
from django.shortcuts import (render, get_object_or_404, 
    redirect)
from django.contrib.auth.forms import AuthenticationForm

#from django.core.paginator import (Paginator, PageNotAnInteger,
#    EmptyPage)

#from models import Event
#from forms import CommentForm, EventForm

def index(request):
    template_name = 'propostaedivida/index.html'
    context = {}   
    return render(request, template_name, context)