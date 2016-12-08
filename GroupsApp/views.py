"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from django.core.exceptions import ObjectDoesNotExist

def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups' : groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        context = {
            'group' : in_group,
            'userIsMember': is_member,
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and request.user.is_student:
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                # checks if a group with the same name already exists
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
                new_group.save()

                # make the creator a member of the group
                new_group.members.add(request.user)
                new_group.save()

                request.user.group_set.add(new_group)
                request.user.save()

                # add the group to the creator's profile
                request.user.group_set.add(new_group)
                request.user.save()

                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'groupformsuccess.html', context)
        else:
            form = forms.GroupForm()
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def deleteGroup(request):
        if request.user.is_authenticated():
                if request.user.is_admin or request.user.is_student:
                        in_name = request.GET.get('name', 'None')

                        group_object = models.Group.objects.get(name__exact=in_name)
			
			try:
				in_group = group_object.members.get(email=request.user.email)
			except ObjectDoesNotExist:
				in_group = None
			
                        if in_group != None or request.user.is_admin:
                                group_object.delete()
                                return render(request, 'groupdeletesuccess.html')
                        else:
                                return render(request, 'memberautherror.html')
                else:
                        return render(request, 'studentautherror.html')
        else:
                return render(request, 'autherror.html')


def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.add(request.user)
        in_group.save();
        request.user.group_set.add(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    
def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.remove(request.user)
        in_group.save();
        request.user.group_set.remove(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': False,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')



def addMemberForm(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            
            form = forms.NewMemberForm(request.POST)
            groupName = request.GET.get('name', 'None')
            currentGroup = models.Group.objects.get(name__exact=groupName)
            
            if form.is_valid() and currentGroup.members.filter(email__exact=request.user.email):    

                # checking if a member with that email exists
                newMemberEmail = form.cleaned_data['email']
                if models.MyUser.objects.filter(email__exact=newMemberEmail): 

                    newMember = models.MyUser.objects.get(email__exact=newMemberEmail)    

                    # adding user to group
                    currentGroup.members.add(newMember)   
                    currentGroup.save() 

                    # adding group to the user
                    newMember.group_set.add(currentGroup)
                    newMember.save()

                    context = {
                        'groupname' : groupName,
                        'newmembername' : newMember.get_full_name
                    }
                    return render(request, 'groupformaddmembersuccess.html', context)
                
                else:
                    groupName = request.GET.get('name', 'None')
            
                    if request.user.group_set.filter(name__exact=groupName):
                        context = {
                            'gname' : groupName
                        }
                        
                        return render(request, 'addMemberForm.html', context)

        else:
            groupName = request.GET.get('name', 'None')
            
            if request.user.group_set.filter(name__exact=groupName):
                context = {
                    'gname' : groupName
                }
                
                return render(request, 'addMemberForm.html', context)
    else:
         return render(request, 'autherror.html')   
    
