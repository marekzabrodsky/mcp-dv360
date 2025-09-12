#!/usr/bin/env python3
"""
Script to generate OAuth refresh token for DV360 API access.
Run this once to get your refresh token for development/testing.
"""

import sys
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/display-video']

def get_refresh_token(client_secrets_file):
    """Get refresh token using OAuth flow."""
    
    print("🔐 Starting OAuth flow for DV360 API...")
    print("📋 This will open your browser for authentication.")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
        credentials = flow.run_local_server(port=8080)
        
        print("\n✅ Authentication successful!")
        print("\n📝 Your OAuth credentials:")
        print(f"Client ID: {credentials.client_id}")
        print(f"Client Secret: {credentials.client_secret}")  
        print(f"Refresh Token: {credentials.refresh_token}")
        
        print("\n🔧 Add these to your .env file:")
        print(f"OAUTH_CLIENT_ID={credentials.client_id}")
        print(f"OAUTH_CLIENT_SECRET={credentials.client_secret}")
        print(f"OAUTH_REFRESH_TOKEN={credentials.refresh_token}")
        
        return credentials
        
    except Exception as e:
        print(f"❌ Error during OAuth flow: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 get_oauth_token.py client_secrets.json")
        print("\n1. Download OAuth credentials from Google Cloud Console")
        print("2. Save as 'client_secrets.json'")
        print("3. Run this script")
        sys.exit(1)
    
    client_secrets_file = sys.argv[1]
    get_refresh_token(client_secrets_file)