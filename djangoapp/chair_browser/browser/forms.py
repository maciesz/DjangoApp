from django import forms
from django.forms import extras
from browser.models import UserProfile, Term
from django.contrib.auth.models import User
from datetime import datetime
import datetime
from browser.select_time_widget import SelectTimeWidget
from django.contrib.admin.widgets import AdminTimeWidget

class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model=User
		fields=('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
	class Meta:
		model=UserProfile
		fields=('photo',)


class TermForm(forms.Form):
	date=forms.DateField(widget=extras.SelectDateWidget())
	from_hour=forms.TimeField(widget=AdminTimeWidget(format='%H:%M'))
	to=forms.TimeField(widget=AdminTimeWidget(format='%H:%M'))
	#from_hour=forms.TimeField(widget=SelectTimeWidget(), label="From")
	#to=forms.TimeField(widget=SelectTimeWidget())


class ContactForm(forms.Form):
    emial=forms.EmailField(label='Your Email')
    subject=forms.CharField()
    message=forms.CharField(widget=forms.Textarea)


