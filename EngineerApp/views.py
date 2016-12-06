from django.shortcuts import render

# Create your views here.
from django.contrib import messages

from . import models
from . import forms
from forms import EngineerUpdateForm
from EngineerApp.models import Engineer


def getEngineers(request):
	if request.user.is_authenticated():
		engineers_list = models.Engineer.objects.all()
		context = {
			'engineers' : engineers_list
		}
		return render(request, 'engineers.html', context)
	else:
		return render(request, 'autherror.html')



def getEngineer(request):
	if request.user.is_authenticated():
		request_email = request.user.email

		try:
			engineer = Engineer.objects.get(email=request_email)
		except Engineer.DoesNotExist:
			return render(request, 'engineerautherror.html')

		context = {
			'engineer' : engineer
		}
		return render(request, 'engineer.html', context)
	else:
		return render(request, 'autherror.html')



def getEngineerForm(request):
	if request.user.is_authenticated():
		# Auto Complete the name and email of request.user
		return render(request, 'engineerform.html')
	else:
		return render(request, 'autherror.html')


def getEngineerFormSuccess(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = forms.EngineerForm(request.POST, request.FILES)
			if form.is_valid():
				# check if an engineer with the same name already exists
				if models.Engineer.objects.filter(name__exact=form.cleaned_data['name']).exists():
					return render(request, 'engineerform.html', {'error': 'Error: The name entered already exists!'})
				else:
					new_engineer = models.Engineer(
							name=form.cleaned_data['name'],
							photo=request.FILES['photo'],
							email=form.cleaned_data['email'],
							user_map=request.user
						)
					new_engineer.save()

					context = {
						'name' : form.cleaned_data['name']
					}
					return render(request, 'engineerformsuccess.html', context)
		else:
			return render(request, 'engineerform.html')
	else:
		return render(request, 'autherror.html')


def updateEngineer(request):
	if request.user.is_authenticated():
		if request.user.is_engineer:
			user_email = request.user.email
			engineer = Engineer.objects.get(email=user_email)
			form = EngineerUpdateForm(request.POST or None, instance=engineer)

			if form.is_valid():
				form.save()
				messages.success(request, 'Success, your profile was saved!')

			context = {
				"form": form,
				"page_name" : "Update Engineer",
				"button_value" : "Update",
				"links" : ["logout"],
			}
			return render(request, 'auth_form.html', context)
		else:
			return render(request, 'engineerautherror.html')	
	else:
		return render(request, 'autherror.html') 





