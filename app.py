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

