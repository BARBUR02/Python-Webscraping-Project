from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Announcement, CustomUser


# Create your forms here.

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)

    
	class Meta:
		model = CustomUser
		fields = ("username", "email", "first_name","last_name", "phone_number" ,"password1", "password2")

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			user = CustomUser.objects.get(email=email)
		except Exception as e:
			return email
		raise forms.ValidationError(f'Email {email} is already is use.')
        
	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			user = CustomUser.objects.get(username=username)
		except Exception as e:
			return username
		raise forms.Validation


class LoginForm(forms.ModelForm):

	password = forms.CharField(label="Password", widget = forms.PasswordInput)

	class Meta:
		model = CustomUser
		fields = ('email', 'password')
	
	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid Login or password")
				

class OfferForm(forms.ModelForm):
	class Meta: 
		model = Announcement
		fields = ('name', 'subject', 'locations', 'minPrice', 'description', 'phone_number')