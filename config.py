import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EdgeConfig:
    def __init__(self):
        self.edge_config_token = os.getenv('EDGE_CONFIG_TOKEN')
        self.edge_config_item_key = os.getenv('EDGE_CONFIG_ITEM_KEY')
        
        # Fallback values
        self.fallback_config = {
            "hotel_name": os.getenv('HOTEL_NAME', 'The Scotsman Hotel'),
            "tagline": os.getenv('TAGLINE', 'Luxury Travel Options to Niagara Falls'),
            "primary_color": os.getenv('PRIMARY_COLOR', '#C5A572'),
            "secondary_color": os.getenv('SECONDARY_COLOR', '#1a1a1a'),
            "logo_url": None,  # Will be populated with local file if Edge Config doesn't have it
            "header_image_url": None,
            "favicon_url": None
        }
    
    def get_branding(self):
        """
        Get branding information from Vercel Edge Config
        Falls back to environment variables if Edge Config is not available
        """
        if not self.edge_config_token or not self.edge_config_item_key:
            print("Edge Config not configured, using fallback values")
            return self.fallback_config
            
        try:
            headers = {
                "Authorization": f"Bearer {self.edge_config_token}"
            }
            
            response = requests.get(
                f"https://api.vercel.com/v1/edge-config/{self.edge_config_item_key}/items",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                # Extract branding information from Edge Config
                branding = {}
                
                # Map Edge Config items to our branding object
                for key in self.fallback_config.keys():
                    if key in data.get('items', {}):
                        branding[key] = data['items'][key]['value']
                    else:
                        branding[key] = self.fallback_config[key]
                
                return branding
            else:
                print(f"Failed to fetch Edge Config: {response.status_code}")
                return self.fallback_config
                
        except Exception as e:
            print(f"Error fetching Edge Config: {str(e)}")
            return self.fallback_config
    
    def update_media_asset(self, asset_key, asset_url):
        """
        Update a media asset URL in Edge Config
        
        Parameters:
        - asset_key: The key for the asset (e.g., 'logo_url')
        - asset_url: The URL to the media asset
        
        Returns:
        - True if successful, False otherwise
        """
        if not self.edge_config_token or not self.edge_config_item_key:
            print("Edge Config not configured, cannot update media asset")
            return False
            
        try:
            headers = {
                "Authorization": f"Bearer {self.edge_config_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "items": [
                    {
                        "operation": "update",
                        "key": asset_key,
                        "value": asset_url
                    }
                ]
            }
            
            response = requests.patch(
                f"https://api.vercel.com/v1/edge-config/{self.edge_config_item_key}/items",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                print(f"Successfully updated {asset_key} in Edge Config")
                return True
            else:
                print(f"Failed to update Edge Config: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error updating Edge Config: {str(e)}")
            return False

# Create a singleton instance
edge_config = EdgeConfig() 