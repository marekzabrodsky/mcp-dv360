# 🚀 Complete Setup Guide - DV360 MCP Server

## ✅ Current Status
- [x] Project created and tested
- [x] Dependencies installed
- [x] MCP server code ready
- [x] Claude Desktop config updated
- [ ] **Google credentials needed**

## 🔐 Final Steps to Complete Setup

### 1. Choose Authentication Method

#### Option A: Service Account (Recommended)
```bash
# 1. Create service account in Google Cloud Console
# 2. Download JSON key file
# 3. Save to secure location (NOT in project!)
# 4. Update Claude config path:
```

Edit this file: `/Users/marekzabrodsky/Library/Application Support/Claude/claude_desktop_config.json`

Replace this line:
```json
"GOOGLE_APPLICATION_CREDENTIALS": "/path/to/your/dv360-credentials.json"
```

With your actual path:
```json
"GOOGLE_APPLICATION_CREDENTIALS": "/Users/marekzabrodsky/.config/dv360/credentials.json"
```

#### Option B: OAuth 2.0 (For testing)
```bash
# 1. Download client_secrets.json from Google Cloud
# 2. Run OAuth script:
cd /Users/marekzabrodsky/Desktop/dv360-mcp-server-claude
python3 get_oauth_token.py client_secrets.json

# 3. Update Claude config with OAuth:
```

Replace the env section in Claude config:
```json
"env": {
  "OAUTH_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
  "OAUTH_CLIENT_SECRET": "your-client-secret", 
  "OAUTH_REFRESH_TOKEN": "your-refresh-token"
}
```

### 2. Enable APIs (if not done already)
```bash
cd /Users/marekzabrodsky/Desktop/dv360-mcp-server-claude
./enable_apis.sh YOUR_PROJECT_ID
```

### 3. Test Configuration
```bash
cd /Users/marekzabrodsky/Desktop/dv360-mcp-server-claude
python3 -c "
from src.dv360_mcp_server.config import Config
config = Config()
print(f'✅ Credentials type: {config.get_credentials_type()}')
print(f'✅ Valid: {config.validate()}')
"
```

### 4. Restart Claude Desktop
1. Close Claude Desktop completely
2. Restart application
3. Check for "dv360-mcp" server in status

## 🎯 Usage Examples

Once setup is complete, you can use these commands in Claude:

**"Show me all my DV360 advertisers"**
- Lists all advertisers in your account

**"Create a new awareness campaign called 'Holiday Sale 2024' under advertiser 12345"**  
- Creates campaign using the create_campaign tool

**"Get performance data for campaign 67890 for the last 30 days"**
- Generates performance report

**"Pause line item 11111"**
- Pauses the specified line item

**"List all my audience segments"**
- Shows available audiences

## 🔧 Troubleshooting

### Server Not Showing in Claude
1. Check Claude config file syntax (use JSON validator)
2. Verify file paths are absolute and correct
3. Check credentials file exists and is readable
4. Restart Claude Desktop completely

### Authentication Errors
1. Verify service account has DV360 access
2. Check API is enabled in Google Cloud
3. Test credentials with config validation script

### API Errors  
1. Verify advertiser IDs are correct
2. Check account permissions in DV360
3. Monitor API quotas in Google Cloud Console

## 📞 Support

- Check logs in Claude Desktop for error messages
- Test server independently: `python3 test_server.py`
- Verify credentials: Run config validation script

## 🎉 You're Ready!

Your DV360 MCP Server is now ready to use with Claude Desktop!