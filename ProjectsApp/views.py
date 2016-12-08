"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from . import models
from .import forms
from forms import ProjectForm, ProjectUpdateForm
from EngineerApp.models import Engineer
from CompaniesApp.models import Company
from django.http import Http404
from BookmarkApp.models import Bookmark

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
	
		bookmarked = True
		
		try:
			existing_obj=request.user.bookmarks.get(project=in_name)
		except ObjectDoesNotExist:
			bookmarked=False
			
		context = {
			'project' : in_project,
			'bookmarked' : bookmarked,
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

def deleteProject(request):
	if request.user.is_authenticated():
		if request.user.is_admin or request.user.is_engineer:
			in_name = request.GET.get('name', 'None')

			project_object = models.Project.objects.get(name__exact=in_name)

			if project_object.created_by == request.user or request.user.is_admin:
				project_object.delete()
				return render(request, 'projectdeletesuccess.html')	
			else:
				return render(request, 'engineerautherror.html')
		else:
			return render(request, 'engineerautherror.html')
	else:
		return render(request, 'autherror.html')

def bookmarkProject(request):
	if request.user.is_authenticated():
		project_name = request.GET.get('name', 'None')
		project_obj = models.Project.objects.get(name=project_name)

		bookmark_new = Bookmark(email=request.user.email, project=project_name)
		bookmark_new.save()
		
		try:
			existing_obj=request.user.bookmarks.get(project=project_name)
		except ObjectDoesNotExist:	
			request.user.bookmarks.add(bookmark_new)
			request.user.save()

		context = {
			'project': project_obj,
			'bookmarked': True,
		}	

		return render(request, 'project.html', context)
	return render(request, 'autherror.html')

def unBookmarkProject(request):
	if request.user.is_authenticated():
		project_name=request.GET.get('name', 'None')
		project_obj = models.Project.objects.get(name=project_name)

		bookmark_obj=request.user.bookmarks.get(project=project_name)
		
		request.user.bookmarks.remove(bookmark_obj)
		bookmark_obj.delete()

		context = {
			'project' : project_obj,
			'bookmarked' : False,
		}
		return render(request, 'project.html', context)
	return render(request, 'autherror.html')

def updateProject(request):
	if request.user.is_authenticated():
		if request.user.is_engineer:
			project_name = request.GET.get('name', 'None')
			project_obj = models.Project.objects.get(name=project_name)
			# Check for groups
			try:
				existing_bookmark = request.user.bookmarks.get(project=project_name)
			except ObjectDoesNotExist:
				existing_bookmark=None
			
			form = ProjectUpdateForm(request.POST or None, instance=project_obj)

			if form.is_valid():
				if form.cleaned_data['name'] != project_name and existing_bookmark != None:
					existing_bookmark.project=form.cleaned_data['name']
					existing_bookmark.save()

				form.save()
				messages.success(request, 'Success, project has been updated!')
				return render(request, 'projectupdatesuccess.html')

			context = {
				"form": form,
				"page_name" : "Update Project",
				"button_value" : "Update",
				"links" : ["logout"],
			}
			return render(request, 'auth_form.html', context)
		return render(request, 'engineerautherror.html')
	return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and request.user.is_student:
            
            projectName = request.GET.get('projectname', 'None')
            current_project = models.Project.objects.get(name__exact=projectName)

            form = forms.GroupForm(request.POST)
            if form.is_valid():

                curr_uni = form.cleaned_data['university']
                curr_group_name = form.cleaned_data['group']
                curr_group = models.Group.objects.get(name__exact=curr_group_name)

                # check if the student is part of the group
                # check if the group is under the university given // not done
                if curr_group.members.filter(email__exact=request.user.email):

                    # assign group to the project
                    project = models.Project.objects.get(name__exact=projectName)
                    project.group = curr_group
                    project.save()

                    # return to success page that takes you to the group page
                    context = {
                        'pname' : projectName,
                        'gname' : curr_group_name
                    }
                    return render(request, 'addgroupsuccess.html', context)

                else:
                    context = {
                        'projectname' : projectName,
                        'error' : 'you are not part of the group you want to add'
                        }
                    return render(request, 'addgroup.html', context)
        else:
            projectName = request.GET.get('projectname', 'None')
            context = {
                    'projectname' : projectName
                }
            return render(request, 'addgroup.html', context)
    else:
        return render(request, 'autherror.html')




