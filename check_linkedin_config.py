"""
Debug script to test LinkedIn OAuth configuration
Run this to see what's being returned from LinkedIn API
"""
import os
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
LINKEDIN_SCOPES = os.getenv("LINKEDIN_SCOPES", "").split(",")

print("=" * 60)
print("LinkedIn OAuth Configuration")
print("=" * 60)
print(f"Client ID: {LINKEDIN_CLIENT_ID[:20]}..." if LINKEDIN_CLIENT_ID else "❌ Missing LINKEDIN_CLIENT_ID")
print(f"Client Secret: {LINKEDIN_CLIENT_SECRET[:20]}..." if LINKEDIN_CLIENT_SECRET else "❌ Missing LINKEDIN_CLIENT_SECRET")
print(f"Redirect URI: {LINKEDIN_REDIRECT_URI}")
print(f"Scopes: {LINKEDIN_SCOPES}")
print("=" * 60)

if not all([LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_REDIRECT_URI]):
    print("\n❌ Missing required environment variables!")
    print("Make sure your .env file contains:")
    print("  - LINKEDIN_CLIENT_ID")
    print("  - LINKEDIN_CLIENT_SECRET")
    print("  - LINKEDIN_REDIRECT_URI")
    print("  - LINKEDIN_SCOPES")
else:
    print("\n✅ All required environment variables are set!")
    print("\nMake sure your LinkedIn app settings match:")
    print(f"  - Authorized redirect URL: {LINKEDIN_REDIRECT_URI}")
    print(f"  - Application type has OAuth 2.0 enabled")
    print(f"  - App has access to 'Sign In with LinkedIn' product")
