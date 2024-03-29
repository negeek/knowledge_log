
from django import forms
from .models import Topic, Entry


class Topicform(forms.ModelForm):
    class Meta:
        model = Topic
        # only text field is displayed from Topic
        fields = ['topic',  'description', 'public']
        labels = {'topic': 'topic title'}  # signifies no label for text field
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['entry']
        labels = {'entry': ''}
        widgets = {'entry': forms.Textarea(
            attrs={'rows': 3, "PlaceHolder": "Today, i learnt about..."})}


class EntryEditForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['entry']
        labels = {'entry': ''}
        widgets = {'entry': forms.Textarea(
            attrs={'rows': 3, "PlaceHolder": "Today, i learnt about...", "autofocus": True, "class": "edit-entry-field"})}
