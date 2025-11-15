from django import forms
from .models import Quiz
from .models import LinkedIn
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields= ["university","field","major","year"]
        labels={
            "university":"University",
            "field":"Career path",
            "major":"Major",
            "year":"Year"
        }

class LinkedInForm(forms.ModelForm):
    class Meta:
        model = LinkedIn
        fields = ["has_experience", "topic_type", "description", "key_learnings", "image"]

    def clean(self):
        cleaned_data = super().clean()
        has_exp = cleaned_data.get("has_experience")
        desc = cleaned_data.get("description")

        if has_exp and not desc:
            self.add_error("description", "Please describe your experience")

        return cleaned_data
        
    
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


class LinkedInPostForm(forms.Form):
    text_input = forms.CharField(widget=forms.Textarea, required=True)
    image = forms.ImageField(required=False)
    