# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Image(models.Model):
	name = models.CharField(max_length=100)
	time_create = models.DateTimeField(auto_now_add=True)
	is_deleted = models.BooleanField(default=False)

class Method(models.Model):
	name = models.CharField(max_length=100)
	time_create = models.DateTimeField(auto_now_add=True)
	is_deleted = models.BooleanField(default=False)

class Vote(models.Model):
	method = models.ForeignKey(Method, db_index=True)
	image = models.ForeignKey(Image, db_index=True)
	vote_number = models.IntegerField()
	time_create = models.DateTimeField(auto_now_add=True)
	is_deleted = models.BooleanField(default=False)