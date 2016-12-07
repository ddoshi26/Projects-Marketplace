"""CSCapstone Views

Created by Harris Christiansen on 9/18/16.
"""
from django.shortcuts import render

def getIndex(request):
	if request.user.is_authenticated():
		name = request.user.first_name
		print('name =' + name)
		usertype = None
		if request.user.is_professor:
			usertype = "teacher"
		elif request.user.is_engineer:
			usertype = "engineer"
		else:
			usertype = "unknown usertype"
		context = {
			'name' : name,
			'usertype' : usertype
		}
		print('usertype =' + usertype)
		return render(request, 'index2.html', context)

	else:
		return render (request, 'index2.html', {})
		#return render(request, 'index.html', {
        #	'foo': 'bar',
    	#})



def getTable(request):
	return render(request, 'table.html')



def getForm(request):
	return render(request, 'form.html')