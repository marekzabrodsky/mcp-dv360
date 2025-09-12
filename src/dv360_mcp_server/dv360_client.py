"""Google Display & Video 360 API client for MCP server."""

import json
import logging
from typing import Any, Dict, List, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .config import Config

logger = logging.getLogger(__name__)

class DV360Client:
    """Client for interacting with Google Display & Video 360 API."""
    
    def __init__(self, config: Config):
        self.config = config
        self.service = None
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def _get_service(self):
        """Get authenticated DV360 service client."""
        if self.service is None:
            def _build_service():
                credentials = self._get_credentials()
                return build(
                    'displayvideo',
                    self.config.api_version,
                    credentials=credentials,
                    cache_discovery=False
                )
            
            self.service = await asyncio.get_event_loop().run_in_executor(
                self.executor, _build_service
            )
        return self.service
    
    def _get_credentials(self):
        """Get Google API credentials based on configuration."""
        cred_type = self.config.get_credentials_type()
        
        if cred_type == "service_account":
            return ServiceAccountCredentials.from_service_account_file(
                self.config.google_application_credentials,
                scopes=[self.config.api_scope]
            )
        elif cred_type == "oauth":
            return Credentials(
                token=None,
                refresh_token=self.config.oauth_refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.config.oauth_client_id,
                client_secret=self.config.oauth_client_secret,
                scopes=[self.config.api_scope]
            )
        else:
            raise ValueError("No valid credentials configured")
    
    async def _execute_request(self, request):
        """Execute API request asynchronously."""
        def _execute():
            try:
                return request.execute()
            except HttpError as e:
                logger.error(f"API request failed: {e}")
                raise
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, _execute
        )
    
    async def list_advertisers(self, partner_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all advertisers in the account."""
        service = await self._get_service()
        
        # If no partner_id provided, try to get all partners first
        if not partner_id:
            try:
                # List partners to get available partner IDs
                partners_request = service.partners().list()
                partners_response = await self._execute_request(partners_request)
                partners = partners_response.get('partners', [])
                
                if not partners:
                    logger.warning("No partners found - service account may not have access")
                    return []
                
                # Use first partner or iterate through all
                partner_id = partners[0].get('partnerId')
                logger.info(f"Using partner ID: {partner_id}")
            except Exception as e:
                logger.error(f"Could not retrieve partners: {e}")
                return []
        
        # List advertisers for the partner
        request = service.advertisers().list(partnerId=partner_id)
        response = await self._execute_request(request)
        return response.get('advertisers', [])
    
    async def list_campaigns(self, advertiser_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List campaigns, optionally filtered by advertiser."""
        service = await self._get_service()
        campaigns = []
        
        if advertiser_id:
            advertisers = [{'advertiserId': advertiser_id}]
        else:
            advertisers = await self.list_advertisers()
        
        for advertiser in advertisers:
            advertiser_id = advertiser['advertiserId']
            request = service.advertisers().campaigns().list(
                advertiserId=advertiser_id
            )
            response = await self._execute_request(request)
            campaigns.extend(response.get('campaigns', []))
        
        return campaigns
    
    async def list_line_items(self, advertiser_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List line items, optionally filtered by advertiser."""
        service = await self._get_service()
        line_items = []
        
        if advertiser_id:
            advertisers = [{'advertiserId': advertiser_id}]
        else:
            advertisers = await self.list_advertisers()
        
        for advertiser in advertisers:
            advertiser_id = advertiser['advertiserId']
            request = service.advertisers().lineItems().list(
                advertiserId=advertiser_id
            )
            response = await self._execute_request(request)
            line_items.extend(response.get('lineItems', []))
        
        return line_items
    
    async def list_audiences(self, advertiser_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List audience segments."""
        service = await self._get_service()
        
        if advertiser_id:
            request = service.firstAndThirdPartyAudiences().list(
                advertiserId=advertiser_id
            )
        else:
            request = service.firstAndThirdPartyAudiences().list()
        
        response = await self._execute_request(request)
        return response.get('firstAndThirdPartyAudiences', [])
    
    async def list_reports(self) -> List[Dict[str, Any]]:
        """List available reports (queries)."""
        service = await self._get_service()
        request = service.queries().list()
        response = await self._execute_request(request)
        return response.get('queries', [])
    
    async def create_campaign(self, advertiser_id: str, campaign_name: str, campaign_goal: str) -> Dict[str, Any]:
        """Create a new campaign."""
        service = await self._get_service()
        
        campaign_body = {
            'displayName': campaign_name,
            'campaignGoal': {
                'campaignGoalType': campaign_goal.upper()
            },
            'entityStatus': 'ENTITY_STATUS_PAUSED'
        }
        
        request = service.advertisers().campaigns().create(
            advertiserId=advertiser_id,
            body=campaign_body
        )
        
        return await self._execute_request(request)
    
    async def update_line_item_targeting(self, line_item_id: str, targeting_options: Dict[str, Any]) -> Dict[str, Any]:
        """Update targeting options for a line item."""
        service = await self._get_service()
        
        # This is a complex operation that would involve multiple API calls
        # to update different targeting types. For now, return a placeholder.
        return {
            'lineItemId': line_item_id,
            'message': 'Targeting update functionality to be implemented',
            'targetingOptions': targeting_options
        }
    
    async def get_campaign_performance(self, campaign_id: str, date_range: str) -> Dict[str, Any]:
        """Get performance metrics for a campaign."""
        service = await self._get_service()
        
        # Create a query for campaign performance
        query_body = {
            'metadata': {
                'title': f'Campaign Performance - {campaign_id}',
                'dataRange': {
                    'range': date_range.upper()
                },
                'format': 'JSON'
            },
            'params': {
                'type': 'STANDARD',
                'groupBys': ['FILTER_CAMPAIGN'],
                'filters': [
                    {
                        'type': 'FILTER_CAMPAIGN',
                        'value': campaign_id
                    }
                ],
                'metrics': [
                    'METRIC_IMPRESSIONS',
                    'METRIC_CLICKS',
                    'METRIC_CTR',
                    'METRIC_TOTAL_CONVERSIONS',
                    'METRIC_REVENUE_ADVERTISER'
                ]
            },
            'schedule': {
                'frequency': 'ONE_TIME'
            }
        }
        
        request = service.queries().create(body=query_body)
        query_response = await self._execute_request(request)
        
        return {
            'campaignId': campaign_id,
            'dateRange': date_range,
            'queryId': query_response.get('queryId'),
            'status': 'Report generation initiated'
        }
    
    async def pause_line_item(self, line_item_id: str) -> Dict[str, Any]:
        """Pause a line item."""
        # Extract advertiser ID from line item ID (format: advertisers/{id}/lineItems/{id})
        parts = line_item_id.split('/')
        if len(parts) >= 4:
            advertiser_id = parts[1]
            line_item_id_only = parts[3]
        else:
            raise ValueError("Invalid line item ID format")
        
        service = await self._get_service()
        
        # First get the current line item
        request = service.advertisers().lineItems().get(
            advertiserId=advertiser_id,
            lineItemId=line_item_id_only
        )
        line_item = await self._execute_request(request)
        
        # Update status to paused
        line_item['entityStatus'] = 'ENTITY_STATUS_PAUSED'
        
        # Update the line item
        request = service.advertisers().lineItems().patch(
            advertiserId=advertiser_id,
            lineItemId=line_item_id_only,
            updateMask='entityStatus',
            body=line_item
        )
        
        return await self._execute_request(request)
    
    async def create_audience_list(self, advertiser_id: str, audience_name: str, audience_type: str) -> Dict[str, Any]:
        """Create a new audience list."""
        service = await self._get_service()
        
        audience_body = {
            'displayName': audience_name,
            'audienceType': audience_type.upper(),
            'description': f'Audience list created via MCP server: {audience_name}'
        }
        
        request = service.firstAndThirdPartyAudiences().create(
            advertiserId=advertiser_id,
            body=audience_body
        )
        
        return await self._execute_request(request)

    # ===== ENHANCED CAMPAIGN FUNCTIONS =====
    
    async def get_campaign_details(self, advertiser_id: str, campaign_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific campaign."""
        service = await self._get_service()
        request = service.advertisers().campaigns().get(
            advertiserId=advertiser_id,
            campaignId=campaign_id
        )
        return await self._execute_request(request)

    async def list_campaigns_for_advertiser(self, advertiser_id: str) -> List[Dict[str, Any]]:
        """List campaigns for a specific advertiser."""
        service = await self._get_service()
        request = service.advertisers().campaigns().list(
            advertiserId=advertiser_id
        )
        response = await self._execute_request(request)
        return response.get('campaigns', [])
    
    async def list_active_campaigns(self, advertiser_id: str) -> List[Dict[str, Any]]:
        """List only active campaigns for an advertiser."""
        campaigns = await self.list_campaigns_for_advertiser(advertiser_id)
        return [c for c in campaigns if c.get('entityStatus') == 'ENTITY_STATUS_ACTIVE']

    async def search_campaigns(self, advertiser_id: str, search_term: str) -> List[Dict[str, Any]]:
        """Search campaigns by name."""
        campaigns = await self.list_campaigns_for_advertiser(advertiser_id)
        search_lower = search_term.lower()
        return [c for c in campaigns if search_lower in c.get('displayName', '').lower()]
    
    # ===== INSERTION ORDERS =====
    
    async def list_insertion_orders(self, advertiser_id: str, campaign_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List insertion orders for advertiser or specific campaign."""
        service = await self._get_service()
        
        if campaign_id:
            request = service.advertisers().insertionOrders().list(
                advertiserId=advertiser_id,
                filter=f'campaignId="{campaign_id}"'
            )
        else:
            request = service.advertisers().insertionOrders().list(
                advertiserId=advertiser_id
            )
        
        response = await self._execute_request(request)
        return response.get('insertionOrders', [])
    
    async def get_insertion_order_details(self, advertiser_id: str, insertion_order_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific insertion order."""
        service = await self._get_service()
        request = service.advertisers().insertionOrders().get(
            advertiserId=advertiser_id,
            insertionOrderId=insertion_order_id
        )
        return await self._execute_request(request)
    
    # ===== LINE ITEMS =====
    
    async def list_line_items_for_io(self, advertiser_id: str, insertion_order_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List line items for advertiser or specific insertion order."""
        service = await self._get_service()
        
        if insertion_order_id:
            request = service.advertisers().lineItems().list(
                advertiserId=advertiser_id,
                filter=f'insertionOrderId="{insertion_order_id}"'
            )
        else:
            request = service.advertisers().lineItems().list(
                advertiserId=advertiser_id
            )
        
        response = await self._execute_request(request)
        return response.get('lineItems', [])
    
    async def get_line_item_details(self, advertiser_id: str, line_item_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific line item."""
        service = await self._get_service()
        request = service.advertisers().lineItems().get(
            advertiserId=advertiser_id,
            lineItemId=line_item_id
        )
        return await self._execute_request(request)
    
    # ===== TARGETING =====
    
    async def get_targeting_options(self, advertiser_id: str, line_item_id: str) -> Dict[str, Any]:
        """Get targeting configuration for a line item."""
        line_item = await self.get_line_item_details(advertiser_id, line_item_id)
        return line_item.get('targetingExpansion', {})
    
    # ===== CREATIVES =====
    
    async def list_creatives(self, advertiser_id: str) -> List[Dict[str, Any]]:
        """List all creatives for an advertiser."""
        service = await self._get_service()
        request = service.advertisers().creatives().list(
            advertiserId=advertiser_id
        )
        response = await self._execute_request(request)
        return response.get('creatives', [])
    
    async def get_creative_details(self, advertiser_id: str, creative_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific creative."""
        service = await self._get_service()
        request = service.advertisers().creatives().get(
            advertiserId=advertiser_id,
            creativeId=creative_id
        )
        return await self._execute_request(request)
    
    # ===== AUDIENCES =====
    
    async def list_audiences_for_advertiser(self, advertiser_id: str) -> List[Dict[str, Any]]:
        """List audience segments for an advertiser."""
        service = await self._get_service()
        request = service.firstAndThirdPartyAudiences().list(
            advertiserId=advertiser_id
        )
        response = await self._execute_request(request)
        return response.get('firstAndThirdPartyAudiences', [])
    
    async def get_audience_details(self, advertiser_id: str, audience_id: str) -> Dict[str, Any]:
        """Get detailed information about an audience."""
        service = await self._get_service()
        request = service.firstAndThirdPartyAudiences().get(
            advertiserId=advertiser_id,
            firstAndThirdPartyAudienceId=audience_id
        )
        return await self._execute_request(request)
    
    # ===== REPORTING =====
    
    async def run_report_query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Run a custom report query."""
        service = await self._get_service()
        request = service.queries().create(body=query_params)
        return await self._execute_request(request)
    
    async def get_report_status(self, query_id: str) -> Dict[str, Any]:
        """Get status of a report query."""
        service = await self._get_service()
        request = service.queries().get(queryId=query_id)
        return await self._execute_request(request)
    
    async def download_report_data(self, query_id: str) -> Dict[str, Any]:
        """Download report data if ready."""
        service = await self._get_service()
        request = service.queries().reports().list(queryId=query_id)
        response = await self._execute_request(request)
        return response.get('reports', [])
    
    async def list_saved_reports(self, advertiser_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List saved reports."""
        service = await self._get_service()
        request = service.queries().list()
        response = await self._execute_request(request)
        queries = response.get('queries', [])
        
        if advertiser_id:
            # Filter by advertiser if specified
            filtered_queries = []
            for query in queries:
                query_advertisers = query.get('params', {}).get('filters', [])
                if any(f.get('value') == advertiser_id for f in query_advertisers 
                       if f.get('type') == 'FILTER_ADVERTISER'):
                    filtered_queries.append(query)
            return filtered_queries
        
        return queries
    
    # ===== HELPER FUNCTIONS =====
    
    async def get_advertiser_summary(self, advertiser_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of an advertiser."""
        try:
            # Get advertiser details
            advertisers = await self.list_advertisers()
            advertiser = next((a for a in advertisers if a.get('advertiserId') == advertiser_id), None)
            
            if not advertiser:
                return {'error': 'Advertiser not found'}
            
            # Get counts of major entities
            campaigns = await self.list_campaigns_for_advertiser(advertiser_id)
            active_campaigns = [c for c in campaigns if c.get('entityStatus') == 'ENTITY_STATUS_ACTIVE']
            insertion_orders = await self.list_insertion_orders(advertiser_id)
            line_items = await self.list_line_items_for_io(advertiser_id)
            creatives = await self.list_creatives(advertiser_id)
            
            return {
                'advertiser': advertiser,
                'summary': {
                    'total_campaigns': len(campaigns),
                    'active_campaigns': len(active_campaigns),
                    'insertion_orders': len(insertion_orders),
                    'line_items': len(line_items),
                    'creatives': len(creatives)
                },
                'recent_campaigns': campaigns[:5]  # Last 5 campaigns
            }
        except Exception as e:
            return {'error': str(e)}
    
    async def get_campaign_performance_summary(self, advertiser_id: str, campaign_id: str, date_range: str = "LAST_30_DAYS") -> Dict[str, Any]:
        """Get quick performance overview for a campaign."""
        try:
            # Get campaign details
            campaign = await self.get_campaign_details(advertiser_id, campaign_id)
            
            # Create performance query
            query_params = {
                'metadata': {
                    'title': f'Performance Summary - {campaign_id}',
                    'dataRange': {'range': date_range},
                    'format': 'JSON'
                },
                'params': {
                    'type': 'STANDARD',
                    'groupBys': ['FILTER_CAMPAIGN'],
                    'filters': [
                        {'type': 'FILTER_ADVERTISER', 'value': advertiser_id},
                        {'type': 'FILTER_CAMPAIGN', 'value': campaign_id}
                    ],
                    'metrics': [
                        'METRIC_IMPRESSIONS',
                        'METRIC_CLICKS',
                        'METRIC_CTR',
                        'METRIC_TOTAL_CONVERSIONS',
                        'METRIC_REVENUE_ADVERTISER',
                        'METRIC_MEDIA_COST_ADVERTISER'
                    ]
                },
                'schedule': {'frequency': 'ONE_TIME'}
            }
            
            query_result = await self.run_report_query(query_params)
            
            return {
                'campaign': campaign,
                'report_query_id': query_result.get('queryId'),
                'status': 'Report generation initiated',
                'date_range': date_range
            }
        except Exception as e:
            return {'error': str(e)}