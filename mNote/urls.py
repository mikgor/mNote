from mNoteapp import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
]
