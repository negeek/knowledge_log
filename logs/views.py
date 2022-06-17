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
# Create your views here.


def index(request):
    return render(request, 'logs/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    return render(request, 'logs/topics.html', {'topics': topics})


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
        topic = self.topicModel.objects.get(id=topic_id)

        # check for user access to the topic
        if self.topicAccess(user, topic) != True:
            return render(request, self.error_template, {})

        # if access is granted
        other_topics = self.otherTopics(user, topic)
        if entry_id:
            entry = self.entryModel.objects.get(id=entry_id)
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
        topic = self.topicModel.objects.get(id=topic_id)
        if entry_id:
            entry = self.entryModel.objects.get(id=entry_id)
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


@login_required
def public_topics(request):
    topics = topics = Topic.objects.filter(public=True).order_by('-date_added')
    return render(request, 'logs/public_topics.html', {'topics': topics})


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = Topicform()
    else:
        form = Topicform(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('logs:topics'))
    return render(request, 'logs/new_topic.html', {'form': form})


# NAIVE ME WIRTIING RUBBISH BELOW
'''
@login_required
def topic(request, topic_id, entry_id=None):
    topic = Topic.objects.get(id=topic_id)
    topics = Topic.objects.order_by('-date_added')
    topics = topics.exclude(topic=topic)
    if entry_id != None:
        
        print(entry.date_added, entry.updated_at)
    else:
        entry = None

    if request.method == 'GET':
        if entry_id == None:
            topic_entries = dict()
            for other_topic in topics:
                if other_topic != topic:
                    if other_topic.public or request.user == other_topic.owner:
                        other_entries = other_topic.entry_set.count()
                        topic_entries[other_topic] = other_entries
                    else:
                        topics = topics.exclude(topic=other_topic)
            if topic.public == True:
                entries = topic.entry_set.order_by('-date_added')
            else:
                if topic.owner != request.user:
                    return render(request, 'logs/error.html', {})
            entries = topic.entry_set.order_by('-date_added')

            form = EntryForm()
            formEdit = None
        else:

            print(topics)
            topic_entries = dict()
            for other_topic in topics:
                if other_topic != topic:
                    if other_topic.public or request.user == other_topic.owner:
                        other_entries = other_topic.entry_set.count()
                        topic_entries[other_topic] = other_entries
                    else:
                        topics = topics.exclude(topic=other_topic)
            if topic.public == True:
                entries = topic.entry_set.order_by('-date_added')
            else:
                if topic.owner != request.user:
                    return render(request, 'logs/error.html', {})
            entries = topic.entry_set.order_by('-date_added')

            form = EntryForm()
            formEdit = EntryEditForm(instance=entry)
    if request.method == 'POST':
        if entry_id == None:
            form = EntryForm(data=request.POST)

            if form.is_valid():
                new_entry = form.save(commit=False)
                new_entry.topic = topic
                new_entry.owner = request.user

                new_entry.save()

                return HttpResponseRedirect(reverse('logs:topic', args=[topic_id]))
        else:
            formEdit = EntryEditForm(instance=entry, data=request.POST)
            if formEdit.is_valid():
                edit = formEdit.save(commit=False)
                edit.edited = True
                edit.save()
                return HttpResponseRedirect(reverse('logs:topic', args=[topic.id]))

    return render(request, 'logs/topic.html', {'topic': topic, 'entries': entries, 'form': form, 'topics': topics, 'topic_entries': topic_entries, 'formEdit': formEdit, 'entryEdit': entry})

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        print(request.POST)
        form = EntryForm(data=request.POST)

        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return HttpResponseRedirect(reverse('logs:topic', args=[topic_id]))
    return render(request, 'logs/new_entry.html', {'form': form, 'topic': topic})

    @login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        return render(request, 'logs/error.html', {})

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('logs:topic', args=[topic.id]))
    return render(request, 'logs/edit_entry.html', {'form': form, 'topic': topic, 'entry': entry})
    @login_required
def topic(request, topic_id):

    topic = Topic.objects.get(id=topic_id)
    topics = Topic.objects.order_by('date_added')
    topics = topics.exclude(topic=topic)

    print(topics)
    topic_entries = dict()
    for other_topic in topics:
        if other_topic != topic:
            if other_topic.public or request.user == other_topic.owner:
                other_entries = other_topic.entry_set.count()
                topic_entries[other_topic] = other_entries
            else:
                topics = topics.exclude(topic=other_topic)
    if topic.public == True:
        entries = topic.entry_set.order_by('date_added')
    else:
        if topic.owner != request.user:
            return render(request, 'logs/error.html', {})
    entries = topic.entry_set.order_by('date_added')

    form = EntryForm()
    if request.method == 'POST':
        form = EntryForm(data=request.POST)

        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return HttpResponseRedirect(reverse('logs:topic', args=[topic_id]))

    return render(request, 'logs/topic.html', {'topic': topic, 'entries': entries, 'form': form, 'topics': topics, 'topic_entries': topic_entries})
    '''
