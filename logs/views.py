#from audioop import reverse
import string
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Topic, Entry
from .forms import EntryForm, Topicform, EntryEditForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
# Create your views here.


class index(TemplateView):
    template_name = 'logs/index.html'


@method_decorator(login_required, name='dispatch')
class topics(View):
    model = Topic
    form = Topicform
    template_name = 'logs/topics.html'

    def get(self, request, public=None, new_topic=None):
        if not new_topic:
            if not public:
                topics = self.model.objects.filter(
                    owner=request.user).order_by('-date_added')
                return render(request, self.template_name, {'topics': topics})
            elif public == 'public':
                topics = self.model.objects.filter(
                    public=True).order_by('-date_added')
                return render(request, self.template_name, {'topics': topics, 'public': public})
            else:
                return render(request, 'logs/error.html', {})
        elif new_topic == 'new_topic':
            form = self.form()
            return render(request, 'logs/new_topic.html', {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('logs:topics'))


@method_decorator(login_required, name='dispatch')
class topic(View):
    topicModel, entryModel = Topic, Entry
    entryForm, editForm = EntryForm, EntryEditForm
    error_template, template_name = 'logs/error.html', 'logs/topic.html'

    def topicAccess(self, user, topic):
        if topic.public == True or topic.owner == user:
            return True
        return False

    def otherTopics(self, user, topic):
        topics = self.topicModel.objects.order_by(
            '-date_added').exclude(topic=topic)
        other_topics = []
        for other_topic in topics:
            if other_topic.public or user == other_topic.owner:
                other_topics.append(other_topic)
        return other_topics

    def get(self, request, topic_id, entry_id=None):
        user = request.user
        topic = get_object_or_404(self.topicModel, id=topic_id)

        # check for user access to the topic
        if self.topicAccess(user, topic) != True:
            return render(request, self.error_template, {})

        # if access is granted
        other_topics = self.otherTopics(user, topic)
        if entry_id:
            entry = get_object_or_404(self.entryModel, id=entry_id)
            entries = topic.entry_set.order_by('-date_added')
            form = self.entryForm()
            formEdit = self.editForm(instance=entry)
        else:
            entry = None
            entries = topic.entry_set.order_by('-date_added')
            form = self.entryForm()
            formEdit = None
        return render(request, self.template_name, {'topic': topic, 'entries': entries, 'form': form, 'other_topics': other_topics, 'formEdit': formEdit, 'entryEdit': entry})

    def post(self, request, topic_id, entry_id=None):
        topic = get_object_or_404(self.topicModel, id=topic_id)
        if entry_id:
            entry = get_object_or_404(self.entryModel, id=entry_id)
            formEdit = self.editForm(instance=entry, data=request.POST)
            if formEdit.is_valid():
                edit = formEdit.save(commit=False)
                edit.edited = True
                edit.save()
                return HttpResponseRedirect(reverse('logs:topic', args=[topic_id]))

        else:
            form = self.entryForm(data=request.POST)
            if form.is_valid():
                new_entry = form.save(commit=False)
                new_entry.topic = topic
                new_entry.owner = request.user
                new_entry.save()
                return HttpResponseRedirect(reverse('logs:topic', args=[topic_id]))
