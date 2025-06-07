import streamlit as st
from PIL import Image

image = Image.open("Banner.jpg")
st.image(image, use_column_width=True)

