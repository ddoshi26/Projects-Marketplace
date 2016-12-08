from django.shortcuts import render

# Create your views here.
from django.contrib import messages

from . import models
#from . import forms

def getBookmarks(request):
	if request.user.is_authenticated():
		context = {
			'user': request.user,
		}

		return render(request, 'bookmarks.html', context)
	return render(request, 'autherror.html')
