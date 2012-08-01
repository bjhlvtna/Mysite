from django import forms

class EditWikiForm(forms.Form):
	title = forms.CharField(label='Page Title')
	content = forms.CharField(label='Contents', widget=forms.Textarea)

class DeleteWikiForm(forms.Form):
	confirm = forms.CharField(initial='/', widget=forms.HiddenInput())
