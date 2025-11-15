from django.urls import path
from .views import take_quiz, home_view, contact, signup, privacy_policy, terms_of_use, linkedin_auth_url, linkedin_callback, generate_and_post
from .form import LoginForm
from django.contrib.auth import views as auth_views

app_name='core'
urlpatterns = [
    path('take_quiz/', take_quiz, name='take_quiz'),
    path('home/', home_view, name='home_view'),
    path('', home_view, name='home_view'),
    path('contact/', contact, name='contact'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('privacy_policy/', privacy_policy, name='privacy_policy'),
    path('terms_of_use/', terms_of_use, name='terms_of_use'),
    path("auth/linkedin/url/", linkedin_auth_url, name="linkedin_auth_url"),
    path("auth/linkedin/callback/", linkedin_callback, name="linkedin_callback"),
    path('logout/', auth_views.LogoutView.as_view(http_method_names=['get', 'post']), name='logout'),
    path('linkedin/post/', generate_and_post, name='linkedin_post'),
]
