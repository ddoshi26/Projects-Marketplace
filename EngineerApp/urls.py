from django.conf.urls import url

from . import views

urlpatterns = [
	# returns a list of all engineers
	url(r'^engineer/all$', views.getEngineers, name='Engineers'),
	# returns an empty form to register as an Engineer
	url(r'^engineer/form$', views.getEngineerForm, name='EngineerForm'),
	# returns form after original form submitted or refreshed
	url(r'^engineer/formsuccess$', views.getEngineerFormSuccess, name='EngineerFormSuccess'),
	# get the profile page for the engineer
	url(r'^engineer$', views.getEngineer, name='Engineer'),
	# form to update the profile of the engineer
	url(r'^engineer/update$', views.updateEngineer, name='UpdateEngineer'),
]