import streamlit as st
from PIL import Image

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
def_list = ["49ers", "Eagles", "Cowboys"]

col1, col2 = st.columns([1, 5])  # adjust ratios as needed

with col1:
    position = st.selectbox(
        " ",
        options=["QB", "RB", "WR", "TE", "FLEX", "DEF"]
    )

with col2:
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
        logo_map = {
    "49ers": "sanfrancisco_49ers_logo.png",
    "Bears": "chicago_bears_logo.png",
    "Bengals": "cincinnati_bengals_logo.png",
    "Bills": "buffalo_bills_logo.png",
    "Broncos": "denver_broncos_logo.png",
    "Browns": "cleveland_browns_logo.png",
    "Buccaneers": "tampa_buccaneers_logo.png",
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
        logo_file = logo_map.get(player, None)

    if logo_file:
        st.image(f"Logos/{logo_file}", width=100)
