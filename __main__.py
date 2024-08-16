from helpers import get_summoner_info, get_match_ids_by_summoner_puuid, get_match_details, get_team_info

summoner_name = "summoner name"
summoner_tag = "summoner tag"
summoner = get_summoner_info(summoner_name, summoner_tag)
print(summoner)

if summoner:
    summoner_match_ids = get_match_ids_by_summoner_puuid(summoner['puuid'], 20)
    print(f"Last 20 Matches: {summoner_match_ids}\n")
    
    if summoner_match_ids:
        for match_id in summoner_match_ids:
            match_data = get_match_details(match_id)
            if match_data:
                team_info = get_team_info(summoner['puuid'], match_data)
                win_status = "Win" if team_info['won'] else "Loss"
                
                print(f"Match ID: {match_id} | Result: {win_status}")
                print("  Team:")
                for teammate in team_info['team']:
                    print(f"     - {teammate}")
                    
                print("  Opponents:")
                for opponent in team_info['opponents']:
                    print(f"     -{opponent}")
                print()
            else:
                print(f"Match ID: {match_id} | Result: Data unavailable\n")
