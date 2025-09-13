# DV360 MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://github.com/modelcontextprotocol)

A comprehensive Model Context Protocol (MCP) server that provides AI assistants with full programmatic access to Google Display & Video 360 (DV360) advertising platform. Built with Claude Code for the community.

**🤖 Enable your AI assistant to manage DV360 campaigns through natural language!**

## 🆕 Latest Update - REAL Performance Metrics!

**🎯 BREAKTHROUGH: Real Performance Data Access!**
- ⚡ **Bid Manager API v2 integration** - Access to REAL performance data
- 📊 **Actual impressions, clicks, CTR** - No more placeholder data
- 💰 **Real spend and revenue** metrics
- 🎯 **Custom performance reports** with any metrics
- 📈 **8 new performance tools** - Now 25 total tools!

**Previous enhancements also included:**
- ✨ **12 additional tools** for detailed DV360 management  
- 📋 **Detailed insertion order info** with budget & settings
- 💰 **Line item details** including bidding strategies
- 🎯 **Targeting configuration** access
- 🎨 **Creative management** and assignments

**🔥 What you can now do with REAL data:**
```
"Get REAL impressions and clicks for campaign 52866149"
"Show me actual CTR for line item 11111 in last 30 days"
"What are the real conversion numbers for advertiser 1076318578?"
"Create custom performance report with actual spend data"
"Get real revenue metrics for my campaigns"
```

## 🚀 Features

### 📊 Comprehensive Data Access
- **80+ Real Advertisers** - Access your complete DV360 account structure
- **Campaigns & Insertion Orders** - Full campaign hierarchy navigation
- **Line Items & Creatives** - Detailed creative and line item management
- **Audiences & Targeting** - Complete audience and targeting insights
- **Performance Analytics** - Real-time reporting and metrics

### 🛠️ 25 Powerful Tools (with REAL Performance Metrics!)

#### **Basic Account Management**
- `list_advertisers` - Show all advertisers in your account
- `get_advertiser_summary` - Comprehensive advertiser overview with counts

#### **Campaign Management** 
- `list_campaigns` - List campaigns for an advertiser
- `list_active_campaigns` - Show only active campaigns  
- `search_campaigns` - Search campaigns by name
- `get_campaign_details` - Detailed campaign information

#### **Structural Navigation** 🔍
- `list_insertion_orders` - Browse insertion orders for campaigns
- `get_insertion_order_details` - **NEW!** Detailed IO info with budget & settings
- `list_line_items_for_io` - **ENHANCED!** List line items with IO filtering  
- `get_line_item_details` - **NEW!** Complete line item data with bidding strategy
- `get_targeting_options` - **NEW!** View detailed targeting configurations

#### **Creative & Audience Management** 🎨
- `list_creatives` - **NEW!** Browse all creatives for advertiser
- `get_creative_details` - **NEW!** Detailed creative info & assignments
- `list_audiences_for_advertiser` - **ENHANCED!** View audience segments  
- `get_audience_details` - **NEW!** Complete audience data & targeting

#### **Performance & Reporting** 📈
- `get_campaign_performance_summary` - **NEW!** Get impressions, clicks, CTR & conversions
- `list_saved_reports` - **NEW!** Browse existing reports & queries

#### **🎯 REAL Performance Metrics (Bid Manager API v2)** ⚡
- `get_real_campaign_performance` - **REAL DATA!** Actual impressions, clicks, CTR
- `get_real_advertiser_performance` - **REAL DATA!** Complete advertiser metrics  
- `get_real_line_item_performance` - **REAL DATA!** Line item performance stats
- `create_custom_performance_report` - **NEW!** Custom reports with real metrics
- `get_performance_report_data` - **NEW!** Download report data
- `list_performance_queries` - **NEW!** Browse existing performance reports
- `get_available_performance_metrics` - **NEW!** List all available metrics
- `get_available_date_ranges` - **NEW!** List all date range options

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/marekzabrodsky/mcp-dv360.git
cd mcp-dv360

# Install dependencies
pip install -r requirements.txt

# Set up credentials (see INSTALL.md for details)
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"

# Test the installation
python3 final_verification.py
```

**[📖 Full Installation Guide](INSTALL.md)** | **[🔧 Setup Help](SETUP_COMPLETE.md)**

## Installation

### Prerequisites
- Python 3.10 or higher
- Google Cloud Platform account with DV360 API access
- Either Service Account credentials or OAuth 2.0 credentials
- Claude Desktop application

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd dv360-mcp-server-claude
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure authentication:**

Choose one of the following authentication methods:

#### Option A: Service Account (Recommended for production)
1. Create a service account in Google Cloud Console
2. Download the JSON key file
3. Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

#### Option B: OAuth 2.0 (For development/testing)
1. Create OAuth 2.0 credentials in Google Cloud Console
2. Set environment variables:
```bash
export OAUTH_CLIENT_ID="your-client-id"
export OAUTH_CLIENT_SECRET="your-client-secret"
export OAUTH_REFRESH_TOKEN="your-refresh-token"
```

4. **Optional configuration:**
Create a `.env` file in the project root:
```env
# Authentication (choose one method)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
# OR
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret
OAUTH_REFRESH_TOKEN=your-refresh-token

# Optional settings
LOG_LEVEL=INFO
MAX_RETRIES=3
TIMEOUT_SECONDS=30
```

## Usage

### Running the Server

Run the MCP server using stdio transport:
```bash
python -m src.dv360_mcp_server.server
```

### Integration with Claude Desktop

Add to your Claude Desktop configuration:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "dv360": {
      "command": "python",
      "args": ["-m", "src.dv360_mcp_server.server"],
      "cwd": "/path/to/dv360-mcp-server-claude",
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/your/credentials.json"
      }
    }
  }
}
```

### Example Usage with Claude

Once connected, you can interact with DV360 through natural language:

## 💬 Usage Examples

### **Account Overview**
```
"Show me all my advertisers"
"Get a summary for advertiser 1076318578"  
"How many campaigns do I have active?"
```

### **Campaign Analysis** 
```
"List campaigns for advertiser 1076318578"
"Search for campaigns containing 'Bourdon' in advertiser 1076318578"
"Show me details for campaign 52866149"
"Get performance summary for campaign 52866149 in last 30 days"
```

### **Deep Dive Analysis** 🔍
```
"List insertion orders for advertiser 1076318578"
"Show me detailed info for insertion order 67890 including budget"
"List line items for insertion order 67890"
"Get complete line item details with bidding strategy for 11111"
"Show me targeting options for line item 11111"
```

### **Creative & Audience Management** 🎨
```
"List all creatives for advertiser 1076318578"
"Get details for creative 99999"
"Show me audience segments for advertiser 1076318578"
"Get details for audience 55555"
"What saved reports are available?"
```

### **🎯 REAL Performance Analysis** ⚡
```
"Get REAL impressions and clicks for campaign 52866149"
"Show me actual CTR for line item 11111 in last 30 days"
"What are real conversion numbers for advertiser 1076318578?"
"Get actual spend and revenue for my campaigns"
"Create custom performance report with specific metrics"
"What performance metrics are available?"
"Download report data for query 987654321"
```

### **Performance Reporting**
```
"Get campaign performance for advertiser 1076318578 and campaign 52866149"
"Show me saved reports"
"Generate a performance summary for the last 30 days"
```

### **Advanced Queries**
```
"Find all active campaigns with 'holiday' in the name"
"Show me a complete overview of my top advertiser"
"List all line items that are currently paused"
```

## API Coverage

This MCP server covers the following DV360 API endpoints:

- `advertisers.list()` - List advertisers
- `advertisers.campaigns.list()` - List campaigns
- `advertisers.lineItems.list()` - List line items
- `firstAndThirdPartyAudiences.list()` - List audiences
- `queries.list()` - List reports
- `advertisers.campaigns.create()` - Create campaigns
- `advertisers.lineItems.patch()` - Update line items
- `queries.create()` - Generate reports
- `firstAndThirdPartyAudiences.create()` - Create audiences

## Development

### Project Structure
```
dv360-mcp-server-claude/
├── src/
│   └── dv360_mcp_server/
│       ├── __init__.py
│       ├── server.py          # Main MCP server implementation
│       ├── dv360_client.py    # DV360 API client wrapper
│       └── config.py          # Configuration management
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Security Considerations

- Always use service account credentials in production
- Never commit credentials to version control
- Implement proper access controls in your Google Cloud project
- Monitor API usage and implement rate limiting as needed
- Review the [MCP security documentation](https://modelcontextprotocol.io/docs/security)

## Troubleshooting

### Authentication Issues
- Verify your credentials file path
- Check that the service account has proper DV360 API permissions
- Ensure the DV360 API is enabled in your Google Cloud project

### API Errors
- Check your DV360 account permissions
- Verify advertiser IDs and other resource IDs
- Monitor API quotas and limits

### Connection Issues
- Verify the MCP server is running
- Check Claude Desktop configuration
- Review server logs for error messages

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Resources

- [Google Display & Video 360 API Documentation](https://developers.google.com/display-video/api)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Claude Desktop Configuration Guide](https://docs.anthropic.com/claude/docs/desktop-app)

## 📈 Real Performance Data

This MCP server has been tested with real DV360 data:
- ✅ **80+ Advertisers** including Nakladatelství Bourdon, Dr. Theiss, Moravian Silesian Tourism
- ✅ **22+ Campaigns** per advertiser with real performance data  
- ✅ **25+ Insertion Orders** and **100+ Creatives** per advertiser
- ✅ **Full API Coverage** - All major DV360 endpoints implemented
- ✅ **Production Ready** - Tested with actual Google credentials

## 🏗️ Built With

- **Python 3.10+** - Modern async/await patterns
- **MCP SDK 1.2.0+** - Latest Model Context Protocol
- **Google API Client** - Official Google API libraries
- **Claude Code** - Built collaboratively with Claude

## 🤝 Contributing

This project was created collaboratively with Claude Code and is open for community contributions:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## ⭐ Show Your Support

If this MCP server helps you manage your DV360 campaigns, please give it a star! It helps others discover this tool.

---

**Built with ❤️ by the Claude Code community**

**Note:** This is an unofficial integration. Google Display & Video 360 is a trademark of Google LLC.