from django.shortcuts import render

# Create your views here.
from . import models
from . import forms

# Create your views here.
def getComments(request):
    comments_list = models.Comment.objects.all()
    context = {
        'comments' : comments_list,
    }
    return render(request, 'comments.html', context)



# def getCommentForm(request):
#     return render(request, 'commentForm.html')



def addComment(request):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            new_comment = models.Comment(comment=form.cleaned_data['comment'])
            new_comment.save()
            comments_list = models.Comment.objects.all()
            context = {
                'comments' : comments_list,
            }
            return render(request, 'comments.html', context)
        else:
            form = forms.CommentForm()
    return render(request, 'commentForm.html')



# to show all comments for a particular group
def getGComments(request):
    groupName = request.GET.get('name', 'None')
    comments_list = models.Comment.objects.filter(group__name=groupName)
    if not comments_list:
        print('comments_list is empty')
    context = {
        'comments' : comments_list,
    }
    return render(request, 'comments.html', context)



# to add a new comment to a group
def addGComment(request):
    if request.method == 'POST' and request.user.is_authenticated():
        print('123')
        form = forms.CommentForm(request.POST)
        groupName = request.GET.get('name', 'None')
        currentGroup = models.Group.objects.get(name__exact=groupName)

        if form.is_valid() and currentGroup.members.filter(email__exact=request.user.email):
            full_name = request.user.first_name + request.user.last_name
            new_comment = models.Comment(
                comment=form.cleaned_data['comment'], 
                group=currentGroup,
                cname=full_name, 
                cemail=request.user.email)
            new_comment.save()
            
            comments_list = models.Comment.objects.filter(group__name=groupName)
            context = {
                'comments' : comments_list,
                'groupname' : groupName
            }
            return render(request, 'comments.html', context)
    else:
        groupName = request.GET.get('name', 'None')
        comments_list = models.Comment.objects.filter(group__name=groupName)
        context = {
            'comments' : comments_list,
            'groupname' : groupName
        }
        return render(request, 'comments.html', context)  






