from django import forms
from .models import Quiz, LinkedInPost
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["university", "field", "major", "year"]
        labels = {
            "university": "University",
            "field": "Career path",
            "major": "Major",
            "year": "Year"
        }
        widgets = {
            "university": forms.TextInput(attrs={
                'placeholder': 'e.g., Florida Atlantic University',
                'class': 'w-full py-2 px-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            "field": forms.TextInput(attrs={
                'placeholder': 'e.g., Software Engineering',
                'class': 'w-full py-2 px-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            "major": forms.TextInput(attrs={
                'placeholder': 'e.g., Computer Science',
                'class': 'w-full py-2 px-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            "year": forms.NumberInput(attrs={
                'min': '1',
                'max': '5',
                'class': 'w-full py-2 px-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g., 3',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance



class SignUpForm(UserCreationForm):
    class Meta:
        model= User
        fields= ('username','email','password1','password2')
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email',
        'class': 'w-full py-4 px-6 rounded-xl',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm your password',
        'class': 'w-full py-4 px-6 rounded-xl',
    }))

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl',
    }))
    