import streamlit as st
from pathlib import Path
from functions.data_loader import load_data, load_boom_inspection_target
from functions.helper import page_config, init_state_boom_inspection
page_config()

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = None
DATA_FILE = BASE_DIR / "data" / "data_inspeksi.json"
image_files = []

state_boom_inspection = init_state_boom_inspection()

boom_data = load_data(DATA_FILE)
boom_target, boom_target_snake = load_boom_inspection_target()

with st.sidebar:
    st.subheader("Gambar1")
    st.subheader("Gambar2")
    st.subheader("Gambar3")

st.title("Inspeksi BOOM")
st.write("Testing")