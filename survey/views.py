# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


def index(request):
	return render(request, "index.html", {})

def label(request):
	return HttpResponse('hello')

def result(request):
	return HttpResponse('hello')