from django.shortcuts import render, redirect
from .form import QuizForm, SignUpForm, LinkedInPostForm
import urllib.parse
from .utils import generate_state
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import UserCreationForm
import requests
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import LinkedInAccount
from .ai_utils import rewrite_post_with_gemini
from .linkedin import post_to_linkedin


# Create your views here.
def take_quiz(request):
    context = {'form': None}
    if request.method == "POST":
        form = QuizForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['form'] = form
            return redirect('core:home_view')
    else:
        form = QuizForm(user=request.user)
        context['form'] = form

    return render(request, 'take_quiz.html', context)
def home_view(request):
    if request.method == "GET":
        return render(request, 'home.html', {})

# def sign_up(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('/home')
#     else:
#         form = UserCreationForm()

#     return render(request, 'sign_up.html', {'form': form})

def contact(request):
    return render(request, 'contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('core:login')
    else:
        form = SignUpForm()
            
    return render(request, 'signup.html', {
        'form': form
    })

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')


@login_required
def linkedin_auth_url(request):
    state = generate_state()
    request.session["linkedin_oauth_state"] = state

    base_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "scope": " ".join(settings.LINKEDIN_SCOPES),
        "state": state,
    }

    auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)


def linkedin_callback(request):
    """
    LinkedIn OAuth2 callback endpoint
    Handles the redirect from LinkedIn after user authorization
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # Store the callback data in session and redirect to login
        request.session['linkedin_callback_code'] = request.GET.get('code')
        request.session['linkedin_callback_state'] = request.GET.get('state')
        return redirect('core:login')
    
    # Verify state token for security
    stored_state = request.session.get("linkedin_oauth_state")
    received_state = request.GET.get("state")

    if stored_state != received_state:
        return HttpResponse("Invalid state token - possible CSRF attack", status=400)

    code = request.GET.get("code")

    # Exchange code for token
    token_resp = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "client_secret": settings.LINKEDIN_CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token_data = token_resp.json()

    access_token = token_data["access_token"]
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data["expires_in"]

    # Get LinkedIn Profile for member ID
    me = requests.get(
        "https://api.linkedin.com/v2/me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    linkedin_id = me["id"]
    linkedin_urn = f"urn:li:person:{linkedin_id}"

    # Save to DB
    account, created = LinkedInAccount.objects.get_or_create(user=request.user)
    account.access_token = access_token
    account.refresh_token = refresh_token
    account.expires_at = timezone.now() + timedelta(seconds=expires_in)
    account.linkedin_member_urn = linkedin_urn
    account.save()

    # Redirect to a success page or post creation
    return render(request, 'linkedin_connected.html', {
        'success': True,
        'message': 'LinkedIn connected successfully! You can now create and post content.'
    })



@login_required
def generate_and_post(request):
    # Check if user has connected LinkedIn
    try:
        account = LinkedInAccount.objects.get(user=request.user)
        linkedin_connected = True
    except LinkedInAccount.DoesNotExist:
        account = None
        linkedin_connected = False

    if request.method == "POST":
        if not linkedin_connected:
            return HttpResponse("Please connect your LinkedIn account first!", status=400)
        
        user_text = request.POST.get("user_text")
        image_file = request.FILES.get("image")  # uploaded file, optional

        # 1. Generate final caption using Gemini
        final_text = rewrite_post_with_gemini(user_text)

        # 2. Save image temporarily
        img_path = None
        if image_file:
            import os
            media_dir = settings.MEDIA_ROOT
            if not os.path.exists(media_dir):
                os.makedirs(media_dir)
            img_path = os.path.join(media_dir, f"temp_{image_file.name}")
            with open(img_path, "wb") as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

        # 3. Post to LinkedIn
        try:
            result = post_to_linkedin(
                user=request.user,
                text=final_text,
                image_path=img_path
            )
            return render(request, "linkedin_connected.html", {
                "success": True,
                "message": "Posted to LinkedIn successfully!",
                "final_text": final_text
            })
        except Exception as e:
            return render(request, "linkedin_connected.html", {
                "success": False,
                "message": f"Error posting to LinkedIn: {str(e)}",
                "final_text": final_text
            })

    return render(request, "generate_post.html", {
        "linkedin_connected": linkedin_connected
    })