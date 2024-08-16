import tkinter as tk
from tkinter import messagebox
from helpers import get_summoner_info, get_match_ids_by_summoner_puuid, get_match_details, get_team_info

def fetch_match_data():
    summoner_name = entry_summoner_name.get()
    summoner_tag = entry_summoner_tag.get()
    
    if not summoner_name or not summoner_tag:
        messagebox.showerror("Input Error", "Please enter both Summoner Name and Tag")
        return
    
    summoner = get_summoner_info(summoner_name, summoner_tag)
    if not summoner:
        messagebox.showerror("Error", "Summoner not found")
        return
    
    summoner_match_ids = get_match_ids_by_summoner_puuid(summoner['puuid'], 20)
    if not summoner_match_ids:
        messagebox.showerror("Error", "No matches found")
        return
    
    text_results.delete(1.0, tk.END)
    
    for match_id in summoner_match_ids:
        match_data = get_match_details(match_id)
        if match_data:
            team_info = get_team_info(summoner['puuid'], match_data)
            win_status = "Win" if team_info['won'] else "Loss"
            results_text = f"Match ID: {match_id} | Result: {win_status}\nTeam:\n" + \
                           "\n".join(f"    - {player}" for player in team_info['team']) + "\n" + \
                           "Opponents:\n" + "\n".join(f"    - {player}" for player in team_info['opponents'])
            text_results.insert(tk.END, results_text + "\n\n")
        else:
            text_results.insert(tk.END, f"Match ID: {match_id} | Result: Data unavailable\n\n")
            
root = tk.Tk()
root.title("League of Legends Match History")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Summoner Name:").grid(row=0, column=0, padx=5, pady=5)
entry_summoner_name = tk.Entry(frame_input)
entry_summoner_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Summoner Tag:").grid(row=1, column=0, padx=5, pady=5)
entry_summoner_tag = tk.Entry(frame_input)
entry_summoner_tag.grid(row=1, column=1, padx=5, pady=5)

btn_fetch = tk.Button(frame_input, text="Fetch Matches", command=fetch_match_data)
btn_fetch.grid(row=2, columnspan=2, pady=10)

text_results = tk.Text(root, width=80, height=20)
text_results.pack(padx=10, pady=10)

root.mainloop()
