# 🚀 DV360 MCP Server Installation Guide

Easy installation guide for the DV360 MCP Server - get AI access to your Display & Video 360 campaigns in minutes!

## 📋 Prerequisites

- **Python 3.10+** installed on your system
- **Google Cloud Platform** account with DV360 API access
- **Claude Desktop** application installed
- **DV360 account** with appropriate permissions

## 🛠️ Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/dv360-mcp-server.git
cd dv360-mcp-server
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Google Credentials

#### Option A: Service Account (Recommended)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create or select a project
3. Enable the DV360 API:
   ```bash
   gcloud services enable displayvideo.googleapis.com
   ```
4. Create a service account:
   - Go to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Download the JSON key file
5. Save credentials securely (NOT in the project folder):
   ```bash
   mkdir -p ~/.config/dv360
   mv ~/Downloads/your-credentials.json ~/.config/dv360/credentials.json
   ```

#### Option B: OAuth 2.0 (For testing)

```bash
# Download client_secrets.json from Google Cloud Console
python3 get_oauth_token.py client_secrets.json
```

### 4. Test the Installation

```bash
# Set your credentials path
export GOOGLE_APPLICATION_CREDENTIALS="~/.config/dv360/credentials.json"

# Run the test
python3 final_verification.py
```

You should see: `🎉 DV360 MCP Server is READY FOR PRODUCTION!`

### 5. Configure Claude Desktop

Add to your Claude Desktop configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "dv360": {
      "command": "python3",
      "args": ["run_server.py"],
      "cwd": "/full/path/to/dv360-mcp-server",
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/your/credentials.json"
      }
    }
  }
}
```

### 6. Restart Claude Desktop

1. Close Claude Desktop completely
2. Restart the application
3. Check that "dv360" server appears in the status

## ✅ Verification

Once configured, test with these commands in Claude:

- **"Show me all my DV360 advertisers"**
- **"Get summary for my first advertiser"**
- **"List campaigns for advertiser [ID]"**

## 🔧 Troubleshooting

### Server Not Showing in Claude
- Verify JSON syntax in config file
- Check that all file paths are absolute
- Ensure credentials file exists and is readable
- Restart Claude Desktop completely

### Authentication Errors
- Verify service account has DV360 access
- Check that DV360 API is enabled in Google Cloud
- Test credentials with: `python3 final_verification.py`

### API Errors
- Verify advertiser IDs in your account
- Check DV360 account permissions
- Monitor API quotas in Google Cloud Console

## 📞 Support

- **Test independently:** `python3 test_server.py`
- **Verify credentials:** `python3 final_verification.py`
- **Check logs:** Claude Desktop shows error messages
- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/dv360-mcp-server/issues)

## 🎉 You're Ready!

Your DV360 MCP Server is now ready to use with Claude Desktop!

Start managing your Display & Video 360 campaigns through natural language commands.