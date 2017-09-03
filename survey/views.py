# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from survey import models
from django.conf import settings
import os 
from random import shuffle
from django.db.models import F
# Create your views here.


def index(request):
	if request.method == 'GET':
		return render(request, "index.html", {})
	else:
		models.Method.objects.all().delete()
		models.Image.objects.all().delete()
		models.Vote.objects.all().delete()
		methods = os.listdir(os.path.join(settings.STATICFILES_DIRS[0], 'img'))
		methods.remove('origin')
		images = os.listdir(os.path.join(settings.STATICFILES_DIRS[0], 'img', 'origin'))
		for method in methods:
			models.Method.objects.create(name=method)
		for image in images:
			models.Image.objects.create(name=image)
		for method in methods:
			for image in images:
				m = models.Method.objects.get(name=method)
				i = models.Image.objects.get(name=image)
				models.Vote.objects.create(method_id=m.id, image_id=i.id, vote_number=0)
		return render(request, "index.html", {})

def label(request):
	if request.method == 'GET':
		images = models.Image.objects.all()
		methods = models.Method.objects.all()
		imagelist = []
		for image in images:
			imagelist.append({
				'path':image.name
				})
		shuffle(imagelist)
		imagelist = imagelist[:settings.IMAGES_EACH_QUERY]
		methodlist = []
		for method in methods:
			file = os.listdir(os.path.join(settings.STATICFILES_DIRS[0], 'img', method.name))[0]
			methodlist.append({
				'name': method.name,
				'prefix': file[:file.index('_')+1]
				})
		return render(request, "label.html", {
			'images':imagelist,
			'methods':methodlist,
			})
	else:
		for key in request.POST:
			if key.endswith('.jpg'):
				m = models.Method.objects.get(name=request.POST[key])
				i = models.Image.objects.get(name=key)
				models.Vote.objects.filter(method_id=m.id, image_id=i.id).update(vote_number=F('vote_number')+1)
		return HttpResponseRedirect("/result/")

def result(request):
	method_ids = models.Method.objects.all().values_list('id', flat=True)
	method_names = list(models.Method.objects.all().values_list('name', flat=True))
	counts = []
	for method_id in method_ids:
		counts.append(sum(list(models.Vote.objects.filter(method_id=method_id).values_list('vote_number', flat=True))))
	percentages = [x / float(sum(counts)) for x in counts]	
	print method_names, method_ids
	return render(request, "result.html", {
		'methods':method_names,
		'counts':counts,
		'percentages':percentages,
		})