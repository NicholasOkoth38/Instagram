from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import Image, Profile, Comment

class RegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']

    def save(self, commit=True):
        user=super().save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user     

class profileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'profile_photo', 'bio']        

class userForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model= User
        fields= ['username', 'email']


class postImageForm(forms.ModelForm):
    class Meta:
        model=Image
        exclude=['profile', 'likes', 'comments']

class commentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.TextInput()
        self.fields['comment'].widget.attrs['placeholder'] = 'Comment here'
    