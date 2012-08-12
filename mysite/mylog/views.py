#-*- coding: utf8 -*-
# Create your views here.
import re
import sys
import datetime
from django.shortcuts import *
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import logout

from mylog.forms import *
from mylog.models import Page


def make_sidebar_category():
	category = re.compile('^((\[[ㄱ-ㅣ가-힣\w]+\])+)')
	pages = Page.objects.all()

	category_items = []
	for page in pages:
		is_title = False
		encoded_title = page.title.encode('utf-8')
		tmp = category.match(encoded_title)
		title = tmp.group()
		# page object의 title를 이용해서 category item 생성
		for category_item in category_items:
			if category_item[0]==title:
				is_title = True

		if is_title==False:
			category_items.append([title, page.id])
			
	return category_items

def make_sidebar_recent_post():
	recent_posts = Page.objects.order_by('update_date').reverse()[0:5]
	return recent_posts

def category_page(request, category_id):

	category_items = []
	category = re.compile('^((\[[ㄱ-ㅣ가-힣\w]+\])+)')
	page = Page.objects.get(id=category_id)
	title = page.title.encode('utf-8')
	tmp = category.match(title)
	category_name = tmp.group()
	print category_name
	pages = Page.objects.all()

	for page in pages:
		encoded_title = page.title.encode('utf-8')
		if encoded_title.find(category_name)!=(-1):
			print encoded_title
			category_items.append([encoded_title, page.id])


	return render_to_response(
		'category_page.html',{
		'page_title':'category',
		'category_items': category_items,
		'recent_posts':  make_sidebar_recent_post(),
		'category_names': make_sidebar_category(),
		},
		context_instance=RequestContext(request)
	)


def main_page(request):
	pages = Page.objects.all();
	latest_page = Page.objects.get(id=(pages.count()-1))
	for page in pages:
		if latest_page.update_date < page.update_date:
			latest_page = page

	return render_to_response(
		'main_page.html',{
#	'user':request.user,
		'page_title': page.title,
		'page_content': page.content,
		'recent_posts':  make_sidebar_recent_post(),
		'category_names': make_sidebar_category(),
		'page_update_date': page.update_date,
		},
		context_instance=RequestContext(request)
	)


def edit_page(request, page_id):
	if request.method=='POST':
		if page_id!='':
			page = Page.objects.get(id=page_id)
			page.content = request.POST['content']
			# author 추가 
		else:
			title = request.POST['title']
			content = request.POST['content']
			# author 추가 
			page = Page(title=title, content=content) 

		page.update_date = datetime.datetime.now()
		page.save();
		return HttpResponseRedirect('/view/'+str(page.id))
	else:
		if page_id!='':
			page = Page.objects.get(id=page_id)
			return render_to_response(
				'edit_page.html',{
				'header_title':'Edit Page',
				'page': page,
				'recent_posts':  make_sidebar_recent_post(),
				'category_names': make_sidebar_category(),
				'title':page.title,
				'exist':'yes',
				'form':EditWikiForm({
					'title':page.title,
					'content':page.content,
					})
				},		
				context_instance=RequestContext(request)
			)
		else:
			print 'create new page'
			return render_to_response(
				'edit_page.html',{
				'header_title':'Edit Page',
				'recent_posts':  make_sidebar_recent_post(),
				'category_names': make_sidebar_category(),
				'exist':'no',
				'form':EditWikiForm()},
				context_instance=RequestContext(request)
			)

def view_page(request, id):
	try:
		page = Page.objects.get(id=id)
	except:
		raise Http404('Page Not found!')

	return render_to_response('view_page.html',{
				'header_title':'view_page',
				'recent_posts':  make_sidebar_recent_post(),
				'category_names': make_sidebar_category(),
				'page_title':page.title,
				'page_content':page.content,
				'page_update_date':page.update_date,
			})

def list_page(request):
	try:
		pages = Page.objects.all()
	except:
		raise Http404('Page Not found')
	
	return render_to_response('list_page.html',{
				'pages':pages,
				'recent_posts':  make_sidebar_recent_post(),
				'category_names': make_sidebar_category(),
			})

def delete_page(request, id):
	try:
		page = Page.objects.get(id=id)
	except:
		raise Http404('Page Not found!')

	if request.method=='POST' and request.POST['confirm']=='/':
		page.delete()
		return HttpResponseRedirect('/list/')
	else:
		form = DeleteWikiForm()
		return render_to_response('delete_page.html',{
				'page_title':page.title,
				'recent_posts':  make_sidebar_recent_post(),
				'category_names': make_sidebar_category(),
				'page':page,
				'form': form },
				context_instance=RequestContext(request)
				
				)

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_page(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password'],
				email = form.cleaned_data['email']
			)
			return HttpResponseRedirect('/register/success/')
	else:
		form = RegistrationForm()

	return render_to_response (
		'registration/register.html',{
		'form':form,
		'recent_posts':  make_sidebar_recent_post(),
		'category_names': make_sidebar_category(),
		},
		context_instance=RequestContext(request)
	)
	


