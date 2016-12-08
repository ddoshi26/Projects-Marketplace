from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^comments/group$', views.getGComments, name='getGComment'),
	url(r'^addcomment/group$', views.addGComment, name='getGComment'),
    url(r'^comments$', views.getComments, name='Comments'),
    # url(r'^commentform$', views.getCommentForm, name='CommentForm'),
    url(r'^addcomment$', views.addComment, name='AddComment'),
]
