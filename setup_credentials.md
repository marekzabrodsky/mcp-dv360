# 🔐 Credentials Setup Guide

## Option A: Service Account (Recommended)

### 1. Create Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **IAM & Admin** → **Service Accounts**
3. Click **"Create Service Account"**
4. Name: `dv360-mcp-server`
5. Description: `Service account for DV360 MCP Server`

### 2. Download JSON Key
1. Click on your service account
2. Go to **Keys** tab
3. Click **"Add Key"** → **"Create New Key"** → **JSON**
4. Save file as `dv360-credentials.json`
5. Move to secure location (NOT in project folder!)

### 3. Set Environment Variable
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/dv360-credentials.json"
```

### 4. Grant DV360 Access
⚠️ **IMPORTANT**: Service account needs to be added to your DV360 account:
1. Go to DV360 interface
2. Settings → User Management
3. Add service account email with appropriate permissions

---

## Option B: OAuth 2.0 (For Testing)

### 1. Create OAuth Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **"Create Credentials"** → **"OAuth 2.0 Client IDs"**
3. Application type: **Desktop application**
4. Name: `DV360 MCP Server OAuth`

### 2. Get Refresh Token
Run this Python script to get refresh token:

```python
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/display-video']
CLIENT_SECRETS_FILE = 'client_secrets.json'  # Downloaded OAuth credentials

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_local_server(port=0)

print(f"Refresh Token: {credentials.refresh_token}")
```

### 3. Set Environment Variables
```bash
export OAUTH_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export OAUTH_CLIENT_SECRET="your-client-secret"
export OAUTH_REFRESH_TOKEN="your-refresh-token"
```

---

## 🔒 Security Best Practices

- ✅ Never commit credentials to git
- ✅ Use environment variables or secure vaults
- ✅ Rotate credentials regularly
- ✅ Use least-privilege access
- ❌ Don't share credentials in plain text
- ❌ Don't store in project directories

---

## 🧪 Test Credentials

Run this test to verify your setup:

```bash
cd /Users/marekzabrodsky/Desktop/dv360-mcp-server-claude
python3 -c "
from src.dv360_mcp_server.config import Config
config = Config()
print(f'Credentials type: {config.get_credentials_type()}')
print(f'Valid: {config.validate()}')
"
```