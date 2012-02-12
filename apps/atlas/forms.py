from django.utils.translation import ugettext_lazy as _
from django import forms
from apps.atlas.models import Spod
from django.contrib.auth.models import User

class SpodForm(forms.ModelForm):
    """
    Spod form
    
    """
    user            = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    title           = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'title text'}))
    spotline        = forms.CharField(widget=forms.Textarea(attrs={'class': 'spotline textarea', 'rows': 3}))
    latitude        = forms.FloatField(widget=forms.HiddenInput)
    longitude       = forms.FloatField(widget=forms.HiddenInput)

    class Meta:
        model       = Spod
        exclude     = ['status']
