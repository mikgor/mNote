from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import *
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note
from django.http import HttpResponseRedirect, HttpResponse

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'mNoteapp/index.html'
    context_object_name = 'index_context'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['notes'] = self.request.user.notes.all()
        context['groups'] = self.request.user.groups.all()
        return context

class GroupListView(LoginRequiredMixin, generic.ListView):
    template_name = 'mNoteapp/groups.html'
    context_object_name = 'groups'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
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
        if not self.object.type == "text":
            self.object.color = "limegreen" if self.object.type == "todo" else "mediumpurple"
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
        if not self.object.type == "text":
            self.object.color = "limegreen" if self.object.type == "todo" else "mediumpurple"
        self.object.groupId = groupid
        self.object.save()
        g = Group.objects.get(id=groupid)
        g.notes.add(self.object)
        notification = '{0} stworzył nową notatkę grupy: {1}'.format(self.request.user.username, self.object.title)
        for user in g.users.all().exclude(username=self.request.user.username):
            user.NewNotification(text=notification)
        return HttpResponseRedirect(self.get_success_url())

class GroupCreate(LoginRequiredMixin, CreateView):
    form_class = GroupCreateForm
    template_name = 'mNoteapp/group_form.html'
    success_url = reverse_lazy('GroupListView')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user.username
        self.object.users.add(self.request.user)
        self.request.user.groups.add(self.object)
        self.object.save()
        notification = '{0} dodał Cię do grupy {1}'.format(self.request.user.username, self.object.name)
        for user in self.object.users.all().exclude(username=self.request.user.username):
            user.groups.add(self.object)
            user.NewNotification(text=notification)
        return HttpResponseRedirect(self.get_success_url())

class GroupUpdate(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupUpdateForm
    template_name = 'mNoteapp/group_update_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        notification = '{0} usunął Cię z grupy {1}'.format(self.request.user.username, self.object.name)
        for user in self.object.users.all():
            if not form.cleaned_data['users'].filter(username=user.username).exists() and not user.username==self.object.owner:
                user.groups.remove(self.object)
                user.NewNotification(text=notification)
                print("Usunięto", user.username)

        notification = '{0} dodał Cię do grupy {1}'.format(self.request.user.username, self.object.name)
        for user in form.cleaned_data['users']:
            if not user.groups.filter(pk=self.object.id).exists():
                user.groups.add(self.object)
                user.NewNotification(text=notification)
                print("Dodano", user.username)

        self.object.users.set(form.cleaned_data['users'])
        if not self.object.users.filter(username=self.object.owner).exists():
            self.object.users.add(self.request.user)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

def UpdateCheckboxNote(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    note = ''
    try:
        note_id = request.GET.get('note_id', None)
        index = request.GET.get('index', None)

        if note_id is not None and index is not None:
            note = Note.objects.get(pk=note_id)
            fields = note.text.split(";")
            index = int(index)
            field = fields[index]
            if "*" in field:
                fields[index] = field.replace("*", "")
            else:
                fields[index] = "*" + field

            note.text = ";".join(str(f) for f in fields)
            note.save()
    except:
        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('index'))

class NoteUpdate(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteCreateUpdateForm
    template_name = 'mNoteapp/note_update_form.html'
    success_url = reverse_lazy('index')

class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('index')

class GroupDelete(DeleteView):
    model = Group
    success_url = reverse_lazy('index')

def GroupLeave(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    group_id = ''
    try:
        group_id = request.GET.get('id', None)
        if group_id is not None:
            group = Group.objects.get(pk=group_id)
            request.user.groups.remove(group)
            group.users.remove(request.user)
    except:
        return HttpResponseRedirect(reverse('GroupListView'))
    return HttpResponseRedirect(reverse('GroupListView'))

def NotificationList(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    id = request.GET.get('uid', None)
    notifications = AppUser.objects.get(pk=id).notifications.filter(read=False)
    return HttpResponse(';'.join('{0}/{1}'.format(n.id, n.text) for n in notifications))

def NotificationRead(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('signup'))
    notification_id = ''
    try:
        notification_id = request.GET.get('id', None)
        if notification_id is not None:
            notification = Notification.objects.get(pk=notification_id)
            notification.read = True
            notification.save()
    except:
        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('index'))
