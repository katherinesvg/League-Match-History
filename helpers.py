import requests 
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
        
    params = {'api_key': settings.API_KEY}
    api_url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{summoner_tag}"
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner data from API: {e}')
        return None
    
    
def get_match_ids_by_summoner_puuid(summoner_puuid, matches_count, region=settings.DEFAULT_REGION):
    # # #
    # Retrieve a list of match IDs for matches recently played by a summoner.
    # Args:
    #       summoner_puuid (str): The puuid (Player Universally Unique ID) of summoner
    #       matches_count (int): The number of match IDs to retrieve
    #       region (str, optional): The region where the summoner is located. Defaults to the value in settings.DEFAULT_REGION
    # Returns:
    #       List or None: A list of match IDs if successful, None is an error occurs during API request
    # Raises:
    #       requests.exceptions.RequestException: If there's an issue with the API request
    # Example:
    #       get_matches_by_summoner('sample_puuid', 10, 'na')
    
    params = {
        'api_key': settings.API_KEY,
        'count': matches_count,
    }
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_puuid}/ids"
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner match data from API: {e}')
        return None
    
    
def get_match_details(match_id, region=settings.DEFAULT_REGION):
    params = {'api_key': settings.API_KEY}
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    
    try:
        response= requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting match data from match ID from API: {e}')
        return None


def get_team_info(summoner_puuid, match_data):
    team_info = {'team': [], 'opponents': [], 'won': False}
                 
    if summoner_puuid in match_data['metadata']['participants']:
        player_index = match_data['metadata']['participants'].index(summoner_puuid)
        player_info = match_data['info']['participants'][player_index]
        team_id = player_info['teamId']
        team_info['won'] = player_info['win']
        
        for participant in match_data['info']['participants']:
            if participant['teamId'] == team_id:
                team_info['team'].append(participant['summonerName'])
            else:
                team_info['opponents'].append(participant['summonerName'])
                
    return team_info
