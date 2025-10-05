import requests
import pandas as pd
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")

def get_team_last_matches(team_id, league_id, season=2025):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {"team": team_id, "league": league_id, "season": season, "last": 5}
    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    return data.get("response", [])

def team_scoring_average(team_id, league_id):
    matches = get_team_last_matches(team_id, league_id)
    if not matches:
        return 0
    goals = [m["teams"]["home"]["goals"]["for"] if m["teams"]["home"]["id"] == team_id else m["teams"]["away"]["goals"]["for"] for m in matches]
    return sum(goals) / len(goals)

def filter_high_scoring_teams(teams):
    """Son 5 maçta 2+ gol atanları bulur"""
    return [t for t in teams if t.get("avg_goals", 0) >= 2]
