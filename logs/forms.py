from django import forms
from matplotlib import widgets
from .models import Topic, Entry

class Topicform(forms.ModelForm):
    class Meta:
        model=Topic
        fields=['topic', 'public', 'description'] #only text field is displayed from Topic
        labels={'topic':''} #signifies no label for text field
        widgets={'description':forms.Textarea(attrs={'cols':80})}
      

class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['entry']
        labels={'entry':''}
        widgets={'entry':forms.Textarea(attrs={'cols':80})}