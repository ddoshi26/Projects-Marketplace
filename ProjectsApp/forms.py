from django import forms

from models import MyUser, Engineer

class ProjectForm(forms.Form):
	name = forms.CharField(label='Name', max_length=200, widget=forms.TextInput, required=True)
	description = forms.CharField(label='Description', max_length=10000, widget=forms.TextInput)
	programming_language = forms.CharField(label='Programming Language', max_length=100, widget=forms.TextInput, required=True)
	experience = forms.IntegerField(label='Experience', widget=forms.NumberInput, required=True)
	skills = forms.CharField(label='Skills', max_length=200, widget=forms.TextInput, required=True)
