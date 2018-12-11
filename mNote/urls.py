from mNoteapp import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
    url(r'groups/$', views.GroupListView.as_view(), name='GroupListView'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'newnote/$', views.NoteCreate.as_view(), name='NoteCreate'),
    url(r'newgroup/$', views.GroupCreate.as_view(), name='GroupCreate'),
    url(r'^(?P<pk>[0-9]+)/groupupdate/$', views.GroupUpdate.as_view(), name='GroupUpdate'),
    url(r'newgroupnote/$', views.GroupNoteCreate.as_view(), name='GroupNoteCreate'),
    url(r'^UpdateCheckboxNote/$', views.UpdateCheckboxNote, name='UpdateCheckboxNote'),
    url(r'^GroupLeave/$', views.GroupLeave, name='GroupLeave'),
    url(r'^(?P<pk>[0-9]+)/noteupdate/$', views.NoteUpdate.as_view(), name='NoteUpdate'),
    url(r'^(?P<pk>[0-9]+)/notedelete/$', views.NoteDelete.as_view(), name='NoteDelete'),
    url(r'^(?P<pk>[0-9]+)/groupdelete/$', views.GroupDelete.as_view(), name='GroupDelete'),
]
