import streamlit as st
from PIL import Image

import pandas as pd
import datetime

from dotenv import load_dotenv
import os

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

import requests

def get_implied_points(team_full_name, opponent_full_name, is_home_team):
    url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "spreads,totals",
        "oddsFormat": "decimal",
        "dateFormat": "iso"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        st.error(f"API error: {response.status_code} — {response.text}")
        return None

    data = response.json()

    # Find the matching game
    for game in data:
        if {game["home_team"].lower(), game["away_team"].lower()} == {team_full_name.lower(), opponent_full_name.lower()}:
            dk = next((b for b in game["bookmakers"] if b["key"] == "draftkings"), None)
            if not dk:
                continue

            spreads = next((m for m in dk["markets"] if m["key"] == "spreads"), None)
            totals = next((m for m in dk["markets"] if m["key"] == "totals"), None)
            if not spreads or not totals:
                continue

            total_points = next((o["point"] for o in totals["outcomes"] if o["name"] == "Over"), None)
            spread_dict = {o["name"]: o["point"] for o in spreads["outcomes"]}

            team_spread = spread_dict.get(team_full_name)
            if team_spread is None or total_points is None:
                return None

            implied_opponent = (total_points - team_spread) / 2
            return round(implied_opponent, 1)

    return None

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

# Load schedule CSV
schedule_df = pd.read_csv("nfl_2025_full_schedule.csv")
offense_df = pd.read_csv("offense_ranks_2024.csv")

# Load 2024 team-level sacks allowed per game
sacks_2024_df = pd.read_csv("2024.aSacks.avg.csv")
# Load 2024 turnovers (giveaways) data
giveaways_2024_df = pd.read_csv('2024.Giveaways.csv')
# Load 2025 turnovers data, if available
try:
    giveaways_2025_df = pd.read_csv('giveaways_2025.csv')
except FileNotFoundError:
    giveaways_2025_df = pd.DataFrame(columns=['Team','Week','Giveaways'])

def get_turnovers_per_game(team_full, current_week, giveaways_2025_df):
    # Week 1: use 2024 average giveaways (turnovers allowed)
    if current_week == 1:
        city = ' '.join(team_full.split()[:-1]).lower()
        row = giveaways_2024_df[giveaways_2024_df['Team'].str.lower() == city]
        if not row.empty:
            return row['Avg Giveaways'].iloc[0]
        return None
    # Week 2: use that team’s Week-1 giveaways
    if current_week == 2:
        row = giveaways_2025_df[
            (giveaways_2025_df['Team'].str.lower() == team_full.lower()) &
            (giveaways_2025_df['Week'] == 1)
        ]
        if not row.empty:
            return row['Giveaways'].iloc[0]
        return None
    # Weeks 3+: average of prior weeks
    past = giveaways_2025_df[
        (giveaways_2025_df['Team'].str.lower() == team_full.lower()) &
        (giveaways_2025_df['Week'] < current_week)
    ]
    if not past.empty:
        return past['Giveaways'].mean()
    return None

# Load 2025 team-level sacks data (update path when available)
try:
    sacks_2025_df = pd.read_csv("sacks_2025.csv")
except FileNotFoundError:
    sacks_2025_df = pd.DataFrame(columns=["Team", "Week", "Sacks"])

def get_sacks_allowed(team_full, current_week, sacks_2025_df):
    # Week 1: use 2024 average
    if current_week == 1:
        # derive city by dropping team nickname from full name
        city = " ".join(team_full.split()[:-1]).lower()
        lookup_name = city
        row = sacks_2024_df[sacks_2024_df["Team"].str.lower() == lookup_name]
        if not row.empty:
            return row["Sacks Allowed Per Game"].iloc[0]
        return None
    # Week 2: use that team’s Week-1 total if available
    if current_week == 2:
        row = sacks_2025_df[
            (sacks_2025_df["Team"].str.lower() == team_full.lower()) &
            (sacks_2025_df["Week"] == 1)
        ]
        if not row.empty:
            return row["Sacks"].iloc[0]
        return None
    # Weeks 3+: average of prior weeks
    past = sacks_2025_df[
        (sacks_2025_df["Team"].str.lower() == team_full.lower()) &
        (sacks_2025_df["Week"] < current_week)
    ]
    if not past.empty:
        return past["Sacks"].mean()
    return None


# Detect current week
def get_current_week(start_date=datetime.date(2025, 9, 4)):
    today = datetime.date.today()
    delta = (today - start_date).days
    return min((delta // 7) + 1, 18)

today = datetime.date.today()
season_start = datetime.date(2025, 9, 4)

if today < season_start:
    current_week = 1
else:
    current_week = get_current_week()

image = Image.open("Banner.jpg")
st.image(image, use_container_width=True)

st.markdown(
    """<style>
    div[data-testid="stHorizontalBlock"] {
        margin-top: -50px;
    }
    </style>""",
    unsafe_allow_html=True
)

qb_list = ["Patrick Mahomes", "Josh Allen", "Jalen Hurts"]
rb_list = ["Christian McCaffrey", "Austin Ekeler", "Derrick Henry"]
wr_list = ["Justin Jefferson", "Tyreek Hill", "Ja'Marr Chase"]
te_list = ["Travis Kelce", "George Kittle", "Mark Andrews"]
def_list = ["49ers", "Bears", "Bengals", "Bills", "Broncos", "Browns", "Buccaneers",
    "Cardinals", "Chargers", "Chiefs", "Colts", "Commanders", "Cowboys",
    "Dolphins", "Eagles", "Falcons", "Giants", "Jaguars", "Jets", "Lions",
    "Packers", "Panthers", "Patriots", "Raiders", "Rams", "Ravens", "Saints",
    "Seahawks", "Steelers", "Texans", "Titans", "Vikings"]

logo_map = {
    "49ers": "sanfrancisco_49ers_logo.png",
    "Bears": "chicago_bears_logo.png",
    "Bengals": "cincinnati_bengals_logo.png",
    "Bills": "buffalo_bills_logo.png",
    "Broncos": "denver_broncos_logo.png",
    "Browns": "cleveland_browns_logo.png",
    "Buccaneers": "tampabay_buccaneers_logo.png",
    "Cardinals": "arizona_cardinals_logo.png",
    "Chargers": "losangeles_chargers_logo.png",
    "Chiefs": "kansas_city_chiefs_logo.png",
    "Colts": "indianapolis_colts_logo.png",
    "Commanders": "washington_commanders_logo.png",
    "Cowboys": "dallas_cowboys_logo.png",
    "Dolphins": "miami_dolphins_logo.png",
    "Eagles": "philadelphia_eagles_logo.png",
    "Falcons": "atlanta_falcons_logo.png",
    "Giants": "newyork_giants_logo.png",
    "Jaguars": "jacksonville_jaguars_logo.png",
    "Jets": "newyork_jets_logo.png",
    "Lions": "detroit_lions_logo.png",
    "Packers": "greenbay_packers_logo.png",
    "Panthers": "carolina_panthers_logo.png",
    "Patriots": "newengland_patriots_logo.png",
    "Raiders": "lasvegas_raiders_logo.png",
    "Rams": "losangeles_rams_logo.png",
    "Ravens": "baltimore_ravens_logo.png",
    "Saints": "neworleans_saints_logo.png",
    "Seahawks": "seattle_seahawks_logo.png",
    "Steelers": "pittsburgh_steelers_logo.png",
    "Texans": "houston_texans_logo.png",
    "Titans": "tennessee_titans_logo.png",
    "Vikings": "minnesota_vikings_logo.png",
}

team_to_abbr = {
    "49ers": "SF", "Bears": "CHI", "Bengals": "CIN", "Bills": "BUF", "Broncos": "DEN",
    "Browns": "CLE", "Buccaneers": "TB", "Cardinals": "ARI", "Chargers": "LAC",
    "Chiefs": "KC", "Colts": "IND", "Commanders": "WAS", "Cowboys": "DAL",
    "Dolphins": "MIA", "Eagles": "PHI", "Falcons": "ATL", "Giants": "NYG",
    "Jaguars": "JAC", "Jets": "NYJ", "Lions": "DET", "Packers": "GB",
    "Panthers": "CAR", "Patriots": "NE", "Raiders": "LV", "Rams": "LAR",
    "Ravens": "BAL", "Saints": "NO", "Seahawks": "SEA", "Steelers": "PIT",
    "Texans": "HOU", "Titans": "TEN", "Vikings": "MIN"
}

abbr_to_team = {
    "SF": "San Francisco 49ers", "CHI": "Chicago Bears", "CIN": "Cincinnati Bengals", "BUF": "Buffalo Bills",
    "DEN": "Denver Broncos", "CLE": "Cleveland Browns", "TB": "Tampa Bay Buccaneers", "ARI": "Arizona Cardinals",
    "LAC": "Los Angeles Chargers", "KC": "Kansas City Chiefs", "IND": "Indianapolis Colts", "WAS": "Washington Commanders",
    "DAL": "Dallas Cowboys", "MIA": "Miami Dolphins", "PHI": "Philadelphia Eagles", "ATL": "Atlanta Falcons",
    "NYG": "New York Giants", "JAC": "Jacksonville Jaguars", "NYJ": "New York Jets", "DET": "Detroit Lions",
    "GB": "Green Bay Packers", "CAR": "Carolina Panthers", "NE": "New England Patriots", "LV": "Las Vegas Raiders",
    "LAR": "Los Angeles Rams", "BAL": "Baltimore Ravens", "NO": "New Orleans Saints", "SEA": "Seattle Seahawks",
    "PIT": "Pittsburgh Steelers", "HOU": "Houston Texans", "TEN": "Tennessee Titans", "MIN": "Minnesota Vikings"
}

col1, col2 = st.columns([1, 5])

with col1:
    position = st.selectbox(" ", options=["QB", "RB", "WR", "TE", "FLEX", "DEF"])

with col2:
    player = None
    if position == "QB":
        player = st.selectbox(" ", qb_list)
    elif position == "RB":
        player = st.selectbox(" ", rb_list)
    elif position == "WR":
        player = st.selectbox(" ", wr_list)
    elif position == "TE":
        player = st.selectbox(" ", te_list)
    elif position == "FLEX":
        player = st.selectbox(" ", rb_list + wr_list + te_list)
    elif position == "DEF":
        player = st.selectbox(" ", def_list)

    if position == "DEF" and player:
        opponent_row = schedule_df[
            (schedule_df["team"] == team_to_abbr.get(player, "")) &
            (schedule_df["week"] == current_week)
        ]
        opponent_abbr = opponent_row["opponent"].values[0] if not opponent_row.empty else ""
        
        team_abbr = team_to_abbr.get(player, "")
        team_full = abbr_to_team.get(team_abbr, "")
        opponent_full = abbr_to_team.get(opponent_abbr, "")

        # Determine if selected defense is the home team
        is_home_team = False
        if not opponent_row.empty:
            is_home_team = opponent_row["home"].values[0] == "home"
            
        
        implied_points = get_implied_points(team_full, opponent_full, is_home_team)
        
        offense_row = offense_df[offense_df["team"] == abbr_to_team.get(opponent_abbr, "")]
        
        total_rank = offense_row["total_offense_rank"].values[0] if not offense_row.empty else "??"
        rush_rank = offense_row["rush_rank"].values[0] if not offense_row.empty else "??"
        pass_rank = offense_row["pass_rank"].values[0] if not offense_row.empty else "??"

        # Emoji indicator based on offensive strength
        if total_rank <= 10:
            indicator = "⛔"
        elif 11 <= total_rank <= 20:
            indicator = "🟡"
        else:
            indicator = "✅"

        # Emoji for rushing offense rank
        if rush_rank <= 10:
            rush_indicator = "⛔"
        elif 11 <= rush_rank <= 20:
            rush_indicator = "🟡"
        else:
            rush_indicator = "✅"

        # Emoji for passing offense rank
        if pass_rank <= 10:
            pass_indicator = "⛔"
        elif 11 <= pass_rank <= 20:
            pass_indicator = "🟡"
        else:
            pass_indicator = "✅"
 
# Show logo in col1 if DEF is selected and player is chosen
if position == "DEF" and player:
    with col1:
        logo_file = logo_map.get(player)
        if logo_file:
            st.image(
                f"Logos/{logo_file}",
                output_format="PNG",
                width=120  # you can tweak this if needed
            )

    # NEW ROW FOR STATS — BELOW EVERYTHING
    col1_stats, col2_stats = st.columns([1, 5])

    with col2_stats:
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        stat_col1, stat_col2 = st.columns(2)

        with stat_col1:
            st.markdown(f'<div style="margin-bottom: -8px;">{indicator} Opponent: {opponent_abbr} - {ordinal(total_rank)} Overall</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="margin-bottom: -8px;">{rush_indicator} Rushing Offense Rank: {ordinal(rush_rank)}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="margin-bottom: -8px;">{pass_indicator} Passing Offense Rank: {ordinal(pass_rank)}</div>', unsafe_allow_html=True)
            
            # Key Offensive Injuries header
            st.markdown(
                "<div style='text-align:left; line-height:1; margin-top:16px;'>"
                "<div style='color:#2ECC40; font-weight:bold; font-size:24px;'>Key Offensive Injuries</div>"
                "</div>",
                unsafe_allow_html=True
            )

        with stat_col2:
            # Dynamic turnovers per game
            turnovers_allowed = get_turnovers_per_game(opponent_full, current_week, giveaways_2025_df)
            turnovers_display = round(turnovers_allowed, 1) if turnovers_allowed is not None else '??'
            st.markdown(f'<div style="margin-bottom: -8px;">🔄 Turnovers Per Game: {turnovers_display}</div>', unsafe_allow_html=True)
            # Dynamic sacks allowed per game
            sacks_allowed = get_sacks_allowed(opponent_full, current_week, sacks_2025_df)
            sacks_display = round(sacks_allowed, 1) if sacks_allowed is not None else "??"
            st.markdown(f'<div style="margin-bottom: -8px;">💥 Sacks Allowed Per Game: {sacks_display}</div>', unsafe_allow_html=True)
            implied_display = implied_points if implied_points is not None else "??"
            st.markdown(f'<div style="margin-bottom: -8px;">🧮 Implied Point Total: {implied_display}</div>', unsafe_allow_html=True)
            
            # Key Injuries header (centered)
            st.markdown(
                """
                <div style='text-align:left; line-height:1; margin-top:16px;'>
                  <div style='color:#FF4136; font-weight:bold; font-size:24px;'>
                    Key Defensive Injuries
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )

