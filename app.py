import streamlit as st
from PIL import Image

image = Image.open("Banner.jpg")
st.image(image, use_container_width=True)

col1, col2 = st.columns([1, 5])  # adjust ratios as needed

with col1:
    position = st.selectbox(
        " ",
        options=["QB", "RB", "WR", "TE", "FLEX", "DEF"]
    )


