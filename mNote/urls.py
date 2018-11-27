from mNoteapp import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'newnote/$', views.NoteCreate.as_view(), name='NoteCreate'),
]
