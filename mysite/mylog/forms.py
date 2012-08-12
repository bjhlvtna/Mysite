#-*- coding: UTF-8 -*-
import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class EditWikiForm(forms.Form):
	title = forms.CharField(label='Page Title')
	content = forms.CharField(label='Contents', widget=forms.Textarea)

class DeleteWikiForm(forms.Form):
	confirm = forms.CharField(initial='/', widget=forms.HiddenInput())

class RegistrationForm(forms.Form):
	username = forms.CharField(label='사용자 이름', max_length=30)
	email = forms.EmailField(label='이메일')
	password = forms.CharField(
			label = '비밀번호',
			widget = forms.PasswordInput()
	)
	password_confirm = forms.CharField(
		label = '비밀번호(확인)',
		widget = forms.PasswordInput()
	)

def clean_password(self):
	if 'password' in self.cleaned_data:
		password = self.cleaned_data['password']
		password_confirm = self.cleaned_data['password_confirm']
		if password == password_confirm:
			return password_confirm

	raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

def clean_username(self):
	username = self.cleaned_data['username']
	if not re.search(r'^\w+$',username):
		raise forms.ValidationError(
			'사용자 이름은 알파벳, 숫자, 밑줄(_)만 가능합니다.')
	try:
		user.objects.get(username=username)
	except ObjectDoesNotExist:
		return username
	raise forms.ValidationError('이미 사용 중인 사용자 이름입니다.')


