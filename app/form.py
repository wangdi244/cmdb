#! /usr/bin/env python 
#encoding=utf-8

from django import forms
from app.models import NewUser

class NewUserForm(forms.ModelForm):
    manage_role = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control usediv'}),
                                  choices =NewUser.manage_choice)
  
    class Meta:
        model = NewUser
        exclude = ['role']
