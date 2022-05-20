from logging import PlaceHolder
from django import forms
from matplotlib import widgets
from .models import Topic, Entry


class Topicform(forms.ModelForm):
    class Meta:
        model = Topic
        # only text field is displayed from Topic
        fields = ['topic', 'public', 'description']
        labels = {'topic': ''}  # signifies no label for text field
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['entry']
        labels = {'entry': ''}
        widgets = {'entry': forms.Textarea(
            attrs={'rows': 3, "PlaceHolder": "Today, i learnt about..."})}
