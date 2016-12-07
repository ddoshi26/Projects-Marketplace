"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render

from . import models
from .import forms
from forms import ProjectForm
from EngineerApp.models import Engineer
from CompaniesApp.models import Company
from django.http import Http404

def getProjects(request):
	projects_list = models.Project.objects.all()
	
	return render(request, 'projects.html', {
        	'projects': projects_list,
	})

def getProjectForm(request):
	if request.user.is_authenticated():
		if request.user.is_engineer == True:
			return render(request, 'projectform.html')
		return render(request, 'engineerautherror.html')
	return render(request, 'autherror.html')

def getProject(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		
		in_project = models.Project.objects.get(name__exact=in_name)

		context = {
			'project' : in_project,
		#	'user_name' :
		}

		return render(request, 'project.html', context)
	return render(request, 'autherror.html')

def getProjectFormSuccess(request):
	if request.user.is_authenticated():
		if request.user.is_engineer:
			if request.method == 'POST':
				form = forms.ProjectForm(request.POST or None)
			
				if form.is_valid():
					if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
						return render(request, 'projectform.html', {'error': 'Error: The project name already exists!'})
					#else
					current_user_email = request.user.email
					#eng_user = Engineer.objects.get(email__exact=current_user_email)
					#eng_user_company = eng_user.company		
			
					new_project = models.Project(name=form.cleaned_data['name'], 
							description=form.cleaned_data['description'],
							programming_language=form.cleaned_data['planguage'],
							experience=form.cleaned_data['exp'],
							skills=form.cleaned_data['skills'],
							created_by=request.user,)
							#company=eng_user_company,)

					new_project.save()			
				
					context = {
						'name': form.cleaned_data['name'],
					}
				
					return render(request, 'projectformsuccess.html', context)

				else:
					#raise Http404
					return render(request, 'projectform.html', {'error': 'Error: Failed to create project'})
			else:
				form=forms.ProjectForm()
			return render(request, 'projectform.html')
		else:
			return render(request, 'engineerautherror.html')
	return render(request, 'autherror.html')
				
							
