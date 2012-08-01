#_*_ coding: UTF-8 _*_
# Create your views here.

import datetime
from django.shortcuts import *
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, Http404


from mylog.forms import *
from mylog.models import Page

def main_page(request):
	output = '''
		<html>
			<head>
				<title>%s</title>
			</head>
			<body>
				<h1>%s</h1><p>%s</p>
			</body>
		</html>
	''' % (
		'my site test',
		'Mysite Test',
		'mysite Test'
	)
	return HttpResponse(output)


def edit_page(request, title):
	if request.method=='POST':
		print 'entrace.....'
		if title=='':
			print 'No title'
			title = request.POST['title']
			content = request.POST['content']
			# author 추가 
			page = Page(title=title, content=content) 
		else:
			print 'Here????'
			page = Page.objects.get(title=title)
			page.content = request.POST['content']
			# author 추가 

		page.update_date = datetime.datetime.now()
		page.save();

		return HttpResponseRedirect('/view/'+title)
	else:
		if title=='':
			return render_to_response(
				'edit_page.html',{
				'header_title':'Edit Page',
				'exist':'no',
				'form':EditWikiForm()},
				context_instance=RequestContext(request)
			)
		else:
			try:
				page = Page.objects.get(title=title)
			except:
				page = Page.objects.set(title=title)

			return render_to_response(
				'edit_page.html',{
				'header_title':'Edit Page',
				'title':title,
				'exist':'yes',
				'form':EditWikiForm({
					'title':page.title,
					'content':page.content,
					})
				},		
				context_instance=RequestContext(request)
			)
def view_page(request, title):
	try:
		page = Page.objects.get(title=title)
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

def delete_page(request, title):
	try:
		page = Page.objects.get(title=title)
	except:
		raise Http404('Page Not found!')

	if request.method=='POST' and request.POST['confirm']=='/':
		page.delete()
		return HttpResponseRedirect('/')
	else:
		form = DeleteWikiForm()
		return render_to_response('delete_page.html',{
				'page_title':title,
				'form': form },
				context_instance=RequestContext(request)
				
				)
