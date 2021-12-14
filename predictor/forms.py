from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
class RegisterForm(ModelForm):
    password2=forms.CharField()
    class Meta:
        model = User
        fields=['username', 'email', 'password', 'password2']
    
    def validate(self,validated_data):
        if(validated_data['password']!=validated_data['password2']):
            return forms.ValidationError('Password mismatch!Please enter again')



class LoginForm(ModelForm):

    class Meta:
        model = User
        fields=['username', 'password']
  