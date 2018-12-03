from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class AppUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = ('username',)

class NoteCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('type', 'title', 'text')
        widgets = {'text': forms.HiddenInput()}

class GroupCreateForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name', 'users')

class GroupUpdateForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name', 'users')
