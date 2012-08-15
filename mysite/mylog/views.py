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
from django.db.models import Q

from mylog.forms import *
from mylog.models import Page
'''
category 먼가 구조가.. 맘에 안든다....
'''

def make_sidebar_category(user_email):
	category = re.compile('^((\[[ㄱ-ㅣ가-힣\w]+\])+)')
	if user_email=='':
		pages = Page.objects.filter(private=False)
	else:
		pages = Page.objects.filter(Q(author=user_email) | Q(private=False))
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
	
	recent_posts = Page.objects.filter(private=False).order_by('update_date').reverse()[0:5]
	return recent_posts

def category_page(request, category_id):

	category_items = []
	category = re.compile('^((\[[ㄱ-ㅣ가-힣\w]+\])+)')
	page = Page.objects.get(id=category_id)
	title = page.title.encode('utf-8')
	tmp = category.match(title)
	category_name = tmp.group()

	if request.user.username=='':
		user_email = ''
		pages = Page.objects.filter(private=False)
	else:
		user_email = request.user.email
		pages = Page.objects.filter(Q(author=request.user.email) | Q(private=False))
	for page in pages:
		encoded_title = page.title.encode('utf-8')
		if encoded_title.find(category_name)!=(-1):
			category_items.append([encoded_title, page.id])


	return render_to_response(
		'category_page.html',{
		'page_title':'category',
		'category_items': category_items,
		'recent_posts':  make_sidebar_recent_post(),
		'category_names': make_sidebar_category(user_email),
		},
		context_instance=RequestContext(request)
	)


def main_page(request):

	if request.user.username=='':
		pages = Page.objects.filter(private=False).order_by('update_date').reverse()
		user_email = ''
	else:
		pages = Page.objects.filter(Q(author=request.user.email) | Q(private=False)).order_by('update_date').reverse()
		user_email = request.user.email
	if pages.count()==0:
		page = Page(title='not exist', content='not exist')
	else:
		page = pages[0]

	return render_to_response(
		'main_page.html',{
		'page': page,
		'page_update_date': page.update_date.strftime('%m/%d/%Y'),
		'user':request.user,
		'recent_posts':  make_sidebar_recent_post(),
		'category_names': make_sidebar_category(user_email),
		},
		context_instance=RequestContext(request)
	)


def edit_page(request, page_id):
	if request.method=='POST':
		if page_id=='':
			page = Page()
			post_data = EditWikiForm(request.POST)
			if post_data.is_valid():
				page.title = post_data.cleaned_data['title']
				page.content = post_data.cleaned_data['content']
				page.private = post_data.cleaned_data['private']
				page.author = request.user.email
		else:
			page = Page.objects.get(id=page_id)
			post_data = EditWikiForm(request.POST)
			if post_data.is_valid():
				page.content = post_data.cleaned_data['content']
				page.private = post_data.cleaned_data['private']

		page.update_date = datetime.datetime.now()
		page.save();
		return HttpResponseRedirect('/view/'+str(page.id))
	else:
		if page_id=='':
			return render_to_response(
				'edit_page.html',{
				'header_title':'Edit Page',
				'exist':'no',
				'recent_posts':  make_sidebar_recent_post(),
				'category_names': make_sidebar_category(''),
				'form':EditWikiForm()},
				context_instance=RequestContext(request)
			)
		else:
			page = Page.objects.get(id=page_id)
			return render_to_response(
				'edit_page.html',{
				'page': page,
				'page_update_date': page.update_date.strftime('%m/%d/%Y'),
				'header_title':'Edit Page',
				'exist':'yes',
				'recent_posts':  make_sidebar_recent_post(),
				'category_names': make_sidebar_category(request.user.email),
				'form':EditWikiForm({
					'title':page.title,
					'content':page.content,
					'private':page.private,
					})
				},		
				context_instance=RequestContext(request)
			)

def view_page(request, id):
	try:
		page = Page.objects.get(id=id)
	except:
		raise Http404('Page Not found!')

	if page.private==True:
		page.title = '비공개 글'
		page.content = '비공개 글'
		return render_to_response('view_page.html',{
					'header_title':'view_page',
					'page':page,
					'page_update_date': page.update_date.strftime('%m/%d/%Y'),
					'user':request.user,
					'recent_posts':  make_sidebar_recent_post(),
					'category_names': make_sidebar_category(''),
				})
	else:
		if request.user.username=='':
			user_email = ''
		else:
			user_email = request.user.email

		return render_to_response('view_page.html',{
					'header_title':'view_page',
					'page':page,
					'page_update_date': page.update_date.strftime('%m/%d/%Y'),
					'user':request.user,
					'recent_posts':  make_sidebar_recent_post(),
					'category_names': make_sidebar_category(user_email),
				})

def list_page(request):
	try:
		if request.user.username=='':
			pages = Page.objects.filter(private=False)
			user_email = ''
		else:
			pages = Page.objects.filter(Q(author=request.user.email) | Q(private=False))
			user_email = request.user.email
	except:
		raise Http404('Page Not found')
	
	return render_to_response('list_page.html',{
				'pages':pages,
				'user':request.user,
				'recent_posts':  make_sidebar_recent_post(),
				'category_names': make_sidebar_category(user_email),
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
				'page':page,
				'form': form, 
				'user':request.user,
				'recent_posts':  make_sidebar_recent_post(),
				'category_names': make_sidebar_category(request.user.email),
				},
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
		'category_names': make_sidebar_category(''),
		},
		context_instance=RequestContext(request)
	)
	


