from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
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
        context['groups'] = self.request.user.groups.all()
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

class GroupNoteCreate(LoginRequiredMixin, CreateView):
    form_class = NoteCreateUpdateForm
    template_name = 'mNoteapp/groupnote_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        groupid = self.request.POST['group']
        self.object = form.save(commit=False)
        self.object.save()
        Group.objects.get(id=groupid).notes.add(self.object)
        return HttpResponseRedirect(self.get_success_url())

class GroupCreate(LoginRequiredMixin, CreateView):
    form_class = GroupCreateForm
    template_name = 'mNoteapp/group_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user.username
        self.object.users.add(self.request.user)
        self.object.save()
        for user in self.object.users.all():
            user.groups.add(self.object)
        return HttpResponseRedirect(self.get_success_url())

class GroupUpdate(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupUpdateForm
    template_name = 'mNoteapp/group_update_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        obj = self.object.users.all()
        self.object = form.save(commit=False)

        for user in obj:
            if not form.cleaned_data['users'].filter(username=user.username).exists() and not user.username==self.object.owner:
                user.groups.remove(self.object)
                print("Usunięto", user.username)

        self.object.users.set(form.cleaned_data['users'])
        if not self.object.users.filter(username=self.object.owner).exists():
            self.object.users.add(self.request.user)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
