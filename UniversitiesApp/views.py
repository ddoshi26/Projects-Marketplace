"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from . import models
from . import forms
from TeacherApp.models import Teacher

def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember': is_member,
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityForm(request):
    if request.user.is_authenticated():
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
                new_university = models.University(name=form.cleaned_data['name'], 
                                             photo=request.FILES['photo'],  
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'universityformsuccess.html', context)
            else:
                return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.add(request.user)
        in_university.save();
        request.user.university_set.add(in_university)	
	request.user.save()

	if request.user.is_professor:
		teacher_object = Teacher.objects.get(email=request.user.email)
		teacher_object.university = in_university
		teacher_object.save()

        context = {
            'university' : in_university,
            'userIsMember': True,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')
    
def unjoinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.remove(request.user)
        in_university.save();
        request.user.university_set.remove(in_university)
        request.user.save()

	if request.user.is_professor:
                teacher_object = Teacher.objects.get(email=request.user.email)
                teacher_object.university = None
                teacher_object.save()

        context = {
            'university' : in_university,
            'userIsMember': False,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')
    
def getCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		is_member = in_course.members.filter(email__exact=request.user.email)
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse' : is_member,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def courseForm(request):
	if request.user.is_authenticated():
	    if request.user.is_professor:
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		context = {
			'university': in_university,
		}
		return render(request, 'courseform.html', context)
    # render error page if user is not logged in
	    return render(request, 'createcourseautherror.html')
	return render(request, 'autherror.html')

def addCourse(request):
	if request.user.is_authenticated():
	   if request.user.is_professor:
		if request.method == 'POST':
			form = forms.CourseForm(request.POST)
			if form.is_valid():
				in_university_name = request.GET.get('name', 'None')
				in_university = models.University.objects.get(name__exact=in_university_name)
				if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
					return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
				new_course = models.Course(tag=form.cleaned_data['tag'],
										   name=form.cleaned_data['name'],
										   description=form.cleaned_data['description'],
										   university=in_university)
				new_course.save()
				in_university.course_set.add(new_course)
				is_member = in_university.members.filter(email__exact=request.user.email)
				context = {
					'university' : in_university,
					'userIsMember': is_member,
				}
				return render(request, 'university.html', context)
			else:
				return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
		else:
			form = forms.CourseForm()
			return render(request, 'courseform.html')
		# render error page if user is not logged in
	   return render(request, 'createcourseautherror.html')
	return render(request, 'autherror.html')
		
def removeCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		
		if request.user.is_admin or request.user.is_professor:
			in_course.delete()

		is_member = in_university.members.filter(email__exact=request.user.email)
		context = {
			'university' : in_university,
			'userIsMember' : is_member,
		}
		return render(request, 'university.html', context)
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def joinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.add(request.user)
		in_course.save();
		request.user.course_set.add(in_course)
		request.user.university_set.add(in_university)
		request.user.save()
		
		if request.user.is_professor:
                	teacher_object = Teacher.objects.get(email=request.user.email)
                	teacher_object.courses.add(in_course)
                	teacher_object.save()		

		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': True,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def unjoinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.remove(request.user)
		in_course.save();
		request.user.course_set.remove(in_course)
		request.user.save()
		
		if request.user.is_professor:
                	teacher_object = Teacher.objects.get(email=request.user.email)
                	teacher_object.courses.remove(in_course)
                	teacher_object.save()	

		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': False,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def getAddStudentsForm(request):
	if request.user.is_authenticated():
		return render(request, 'addstudents.html')
	return render(request, 'autherror.html')

def addStudentsFormSuccess(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			if request.user.is_professor == True:
				form = forms.AddStudentsForm(request.POST)
				if form.is_valid():
					in_university_name = form.cleaned_data['university']
					
					try:
						in_university = models.University.objects.get(name__exact=in_university_name)
					except ObjectDoesNotExist:
						return render(request, 'addstudents.html', {'error': 'University Name is invalid'})

					in_course_id = form.cleaned_data['course']
					
					try:
						in_course = models.Course.objects.get(tag__exact=in_course_id)
					except ObjectDoesNotExist:
						return render(request, 'addstudents.html', {'error': 'Course Tag is invalid'})
					
					in_user_email = form.cleaned_data['email']
					
					try:
						in_user=models.MyUser.objects.get(email__exact=in_user_email)
					except ObjectDoesNotExist:
						return render(request, 'addstudents.html', {'error': 'User with email provided does not exist'})

					if in_user.is_student:
						in_university.members.add(in_user)
						in_course.members.add(in_user)
						
						context = {
							'name' : in_university_name,
						}

						return render(request, 'addstudentsuccess.html', context)
					else:
						return render(request, 'notstudenterror.html')
				else:
					return render(request, 'addstudents.html', {'error' : 'Error: Invalid inputs'})
			else:
				return render(request, 'createcourseautherror.html')
		else:
			form = forms.AddStudentsForm()
			return render(request, 'addstudents.html')
	return render(request, 'autherror.html')							
