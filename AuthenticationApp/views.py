"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from .forms import LoginForm, RegisterForm, UpdateForm
from .models import MyUser
from TeacherApp.models import Teacher

# Auth Views

def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if next_url is None:
		next_url = "/"
	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			messages.success(request, 'Success! Welcome, '+(user.first_name or ""))
			login(request, user)
			return HttpResponseRedirect(next_url)
		else:
			messages.warning(request, 'Invalid username or password.')
			
	context = {
		"form": form,
		"page_name" : "Login",
		"button_value" : "Login",
		"links" : ["register"],
	}
	return render(request, 'auth_form.html', context)

def auth_logout(request):
	logout(request)
	messages.success(request, 'Success, you are now logged out')
	return render(request, 'index2.html')

def auth_register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		new_user = MyUser.objects.create_user(
			email=form.cleaned_data['email'], 
			password=form.cleaned_data["password2"], 
			first_name=form.cleaned_data['firstname'], 
			last_name=form.cleaned_data['lastname'],
    		is_student=form.cleaned_data['student'], 
    		is_professor=form.cleaned_data['professor'], 
    		is_engineer=form.cleaned_data['engineer'])
		new_user.save()	

		# logging in
		user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data["password2"])
		
		if user is not None:
			login(request, user)
			messages.success(request, 'Success! Welcome, ' + (user.first_name or "") + ' ' + (user.last_name or ""))
			if form.cleaned_data['professor']==True:
				return render(request, 'teacherform.html')
			elif form.cleaned_data['engineer']==True:
				return render(request, 'engineerform.html')
			else:
				return render(request, 'index.html')
		else:
			print "Big time error"
			
	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'auth_form.html', context)

@login_required
def update_profile(request):
	old_email = request.user.email
	form = UpdateForm(request.POST or None, instance=request.user)
	if form.is_valid():
		if form.cleaned_data['email'] != old_email:
			teacher_obj = Teacher.objects.get(email=old_email)
			teacher_obj.email = form.cleaned_data['email']
			teacher_obj.save()
		
		form.save()
		messages.success(request, 'Success, your profile was saved!')

		teacher_obj2= Teacher.objects.get(email=request.user.email)
		teacher_obj2.user_map=request.user
	context = {
		"form": form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'auth_form.html', context)
