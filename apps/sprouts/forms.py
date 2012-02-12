from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from apps.sprouts.models import Sprout, Branch
from apps.ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField


class SproutForm(forms.ModelForm):
    user            = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    title           = forms.CharField(max_length=128, widget=forms.TextInput(attrs={
                                                        'class': 'title text',
                                                        'placeholder': _('Type your sprout title')
                                                        }))

    class Meta:
        model       = Sprout
        exclude     = ['slug', 'branches', 'tags', 'date_created', 'is_public']

class BranchForm(forms.ModelForm):
    user            = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    source          = forms.ModelChoiceField(queryset=Sprout.objects.all(), widget=forms.HiddenInput)
    target          = AutoCompleteSelectField('target', widget=forms.TextInput(attrs={
                                                        'class': 'branch text'
                                                        }))

    class Meta:
        model       = Branch
        exclude     = ['date_created']
