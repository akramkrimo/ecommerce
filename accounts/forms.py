from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
        )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
        )
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial['password']

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
        attrs = {
            'class': 'form-control ml-0',
        }
    ))

    password = forms.CharField(
        label='Enter Password',
        widget=forms.PasswordInput(
        attrs = {
           'class': 'form-control',
        }
    ))


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match please try again")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']