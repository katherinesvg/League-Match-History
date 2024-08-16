import requests 
from urllib.parse import urlencode
import settings

def get_summoner_info(summoner_name=None, summoner_tag=None, region=settings.DEFAULT_REGION_CODE):
    # # #
    # Wrapper for SUMMONER-V4 API portal
    # Gets info about a summoner by their name
    # :return: Summoner info as a dictionary or None if there's an issue
    # # #
    
    if not summoner_name or not summoner_tag:
        summoner_name = input("Summoner Name:")
        summoner_tag = input("Summoner Tagline:")
        
    params = {
        'api_key': settings.API_KEY
    }
    api_url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{summoner_tag}"
    
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner data from API: {e}')
        return None