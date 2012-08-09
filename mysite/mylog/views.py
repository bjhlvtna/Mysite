#*_ coding: UTF-8 _*_
# Create your views here.

import datetime
from django.shortcuts import *
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import logout

from mylog.forms import *
from mylog.models import Page

def main_page(request):

	pages = Page.objects.all();
	latest_page = Page.objects.get(id=(pages.count()-1))
	for page in pages:
		if latest_page.update_date < page.update_date:
			latest_page = page

	return render_to_response(
		'main_page.html',{
#	'user':request.user,
		'page_title':page.title,
		'page_content':page.content,
		'page_update_date':page.update_date,
		},
		context_instance=RequestContext(request)
	)


def edit_page(request, id):
	if request.method=='POST':
		if Page.objects.filter(id=id).exists():
			page = Page.objects.get(id=id)
			page.content = request.POST['content']
			# author 추가 
		else:
			title = request.POST['title']
			content = request.POST['content']
			# author 추가 
			page = Page(title=title, content=content) 

		page.update_date = datetime.datetime.now()
		page.save();

		return HttpResponseRedirect('/view/'+id)
	else:
		if Page.objects.filter(id=id).exists():
			
			page = Page.objects.get(id=id)
			return render_to_response(
				'edit_page.html',{
				'header_title':'Edit Page',
				'page': page,
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
			return render_to_response(
				'edit_page.html',{
				'header_title':'Edit Page',
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
		'form':form
		},
		context_instance=RequestContext(request)
	)
