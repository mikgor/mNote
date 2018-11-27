from django.views import generic
from django.views.generic.edit import CreateView
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note
from django.http import HttpResponseRedirect

class IndexView(generic.ListView):
    template_name = 'mNoteapp/index.html'
    context_object_name = 'index_context'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['notes'] = self.request.user.notes.all()
        return context

class SignUp(CreateView):
    form_class = AppUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class NoteCreate(LoginRequiredMixin, CreateView):
    form_class = NoteCreateUpdateForm
    template_name = 'mNoteapp/note_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.request.user.notes.add(self.object)
        return HttpResponseRedirect(self.get_success_url())
