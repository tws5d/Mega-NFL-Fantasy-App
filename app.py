import streamlit as st
from PIL import Image

image = Image.open("Banner.jpg")
st.image(image, use_container_width=True)

position = st.selectbox(
    "Choose a position:",
    options=["QB", "RB", "WR", "TE", "FLEX", "DEF"]
)

