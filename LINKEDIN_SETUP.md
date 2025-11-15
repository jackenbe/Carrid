# LinkedIn Integration Setup Guide

## Overview
This application uses LinkedIn OAuth 2.0 to authenticate users and allow them to post content directly to LinkedIn.

## Environment Variables Required

Your `.env` file must contain the following (keep this file secret!):

```
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8000/auth/linkedin/callback/
LINKEDIN_SCOPES=openid,email,profile
ADK_API_KEY=your_gemini_api_key_here
```

## LinkedIn App Configuration

### Step 1: Create a LinkedIn App
1. Go to https://www.linkedin.com/developers/apps
2. Click "Create an app"
3. Fill in the required information
4. Agree to terms and create the app

### Step 2: Configure Authorized Redirect URLs
1. In your app settings, go to the "Auth" tab
2. Under "Authorized redirect URLs for your app", add:
   - `http://localhost:8000/auth/linkedin/callback/` (for local development)
   - `https://yourdomain.com/auth/linkedin/callback/` (for production)

### Step 3: Get Your Credentials
1. Go to the "Auth" tab
2. Copy your:
   - **Client ID** → Put in LINKEDIN_CLIENT_ID
   - **Client Secret** → Put in LINKEDIN_CLIENT_SECRET

### Step 4: Request Sign In with LinkedIn Product
1. Go to the "Products" tab
2. Request access to **"Sign In with LinkedIn"** (formerly "LinkedIn Login")
3. Wait for approval (usually instant or within a few hours)

### Step 5: Configure Required Scopes
1. Go to the "Auth" tab
2. Under "Authorized scopes", make sure you have at least:
   - `openid`
   - `email`
   - `profile`

These scopes allow:
- `openid` - Basic OpenID authentication
- `email` - Access to user's email address
- `profile` - Access to user's basic profile info (name, ID, etc.)

For posting to LinkedIn, you'll also eventually need (request separately):
- `w_member_social` - Permission to post on behalf of the user

## Common Issues

### KeyError: 'id'
**Cause**: The LinkedIn API didn't return an 'id' field
**Solutions**:
1. Check that your app has "Sign In with LinkedIn" product approved
2. Verify scopes include at least: `openid,email,profile`
3. Check the Django console output for the full API response

### 401 Unauthorized
**Cause**: Invalid access token or expired credentials
**Solution**: Make sure LINKEDIN_CLIENT_SECRET is correct

### Invalid state token
**Cause**: Session was cleared or request was forged
**Solution**: This is normal if you restart the server - just try logging in again

### Redirect URL Mismatch
**Cause**: The callback URL doesn't match LinkedIn app settings
**Solution**: Make sure LINKEDIN_REDIRECT_URI exactly matches what's in your LinkedIn app

## Testing the Integration

1. Make sure you're logged into the Carrid app
2. Click "Connect LinkedIn" button
3. You'll be redirected to LinkedIn to authorize
4. After authorization, you should see a success message
5. Your LinkedIn account is now connected!

## Debugging

If you encounter issues, check:
1. Django console output - detailed error messages are printed
2. Your `.env` file has all required variables
3. LinkedIn app is in production (not sandbox)
4. Your scopes are correctly set
5. Your redirect URL matches exactly

Run the config checker:
```bash
python check_linkedin_config.py
```

## Security Note

NEVER commit your `.env` file to Git! It contains sensitive credentials.
Always keep `ADK_API_KEY`, `LINKEDIN_CLIENT_SECRET`, etc. private.
