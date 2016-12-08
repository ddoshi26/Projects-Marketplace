from django import forms

from models import MyUser
from EngineerApp.models import Engineer

class ProjectForm(forms.Form):
	name = forms.CharField(label='Name', max_length=200, widget=forms.TextInput, required=True)
	description = forms.CharField(label='Description', max_length=10000, widget=forms.TextInput)
	planguage = forms.CharField(label='Programming Language', max_length=100, widget=forms.TextInput, required=True)
	exp = forms.CharField(label='Experience', max_length=200, widget=forms.TextInput)
	skills = forms.CharField(label='Skills', max_length=200, widget=forms.TextInput, required=True)

class GroupForm(forms.Form):
	university = forms.CharField(label='University', max_length=200, widget=forms.TextInput, required=True)
	group = forms.CharField(label='Group', max_length=200, widget=forms.TextInput, required=True)