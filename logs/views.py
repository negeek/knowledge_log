#from audioop import reverse
import string
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Topic, Entry
from .forms import EntryForm, Topicform
from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.


def index(request):
    return render(request, 'logs/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    topic_entries = dict()
    for topic in topics:
        entries = topic.entry_set.count()
        topic_entries[topic] = entries

    return render(request, 'logs/topics.html', {'topic_entries': topic_entries, 'topics': topics})


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.public == True:
        entries = topic.entry_set.order_by('date_added')
    else:
        if topic.owner != request.user:
            return render(request, 'logs/error.html', {})
    entries = topic.entry_set.order_by('date_added')

    return render(request, 'logs/topic.html', {'topic': topic, 'entries': entries})


@login_required
def public_topics(request):
    topics = topics = Topic.objects.filter(public=True).order_by('date_added')
    topic_entries = dict()
    for topic in topics:
        entries = topic.entry_set.count()
        topic_entries[topic] = entries
    return render(request, 'logs/public_topics.html', {'topics': topics, 'topic_entries': topic_entries})


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = Topicform()
    else:
        # print(request.POST)
        form = Topicform(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('logs:topics'))
    return render(request, 'logs/new_topic.html', {'form': form})


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
