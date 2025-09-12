#!/bin/bash

# Script to enable required Google APIs for DV360 MCP Server
# Run: ./enable_apis.sh YOUR_PROJECT_ID

PROJECT_ID=$1

if [ -z "$PROJECT_ID" ]; then
    echo "Usage: ./enable_apis.sh YOUR_PROJECT_ID"
    exit 1
fi

echo "🔧 Enabling APIs for project: $PROJECT_ID"

# Enable required APIs
gcloud services enable displayvideo.googleapis.com --project=$PROJECT_ID
gcloud services enable oauth2.googleapis.com --project=$PROJECT_ID  
gcloud services enable iam.googleapis.com --project=$PROJECT_ID

echo "✅ APIs enabled successfully!"
echo "📝 Next: Set up credentials in Google Cloud Console"