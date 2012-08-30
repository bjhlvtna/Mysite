#-*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

# Create your models here.
class Page(models.Model):
	title = models.CharField(unique=True, max_length=128)
	private = models.BooleanField(default=False)
	content = models.TextField()
	author = models.EmailField()
	update_date = models.DateTimeField(auto_now_add=True, blank=True)
#   -------------------------------------------------
	comments = models.PositiveSmallIntegerField(default=0, null=True)

	def __unicode(self):
		return unicode("title : %s " % (self.title))

class Comment(models.Model):
	author = models.CharField(max_length=30, null=False)
	passwd = models.CharField(max_length=10, null=False)
	body = models.TextField(max_length=2000, null=False)
	created_date = models.DateTimeField(auto_now_add=True)
	page = models.ForeignKey(Page)

	def __unicode__(self):
		return unicode("%s : %s : %s" % (self.author, self.passwd, self.body[:60]))

