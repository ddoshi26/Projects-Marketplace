from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^project/all$', views.getProjects, name='Projects'),
    url(r'^project/projectform$', views.getProjectForm, name='ProjectForm'),
    url(r'^project$', views.getProject, name='Project'),
    url(r'^project/formsuccess$', views.getProjectFormSuccess, name='ProjectFormSuccess'),
    url(r'^project/delete$', views.deleteProject, name='DeleteProject'),
    url(r'^project/bookmark$', views.bookmarkProject, name='BookmarkProject'),
    url(r'^project/unbookmark$', views.unBookmarkProject, name='UnBookmarkProject'),
    url(r'^project/update$', views.updateProject, name='UpdateProject'),
]
