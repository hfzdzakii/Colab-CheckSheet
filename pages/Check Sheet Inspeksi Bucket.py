import streamlit as st
from pathlib import Path
from functions.data_loader import load_data, load_bucket_inspection_target
from functions.helper import page_config, init_state_bucket_inspection
page_config()

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = None
DATA_FILE = BASE_DIR / "data" / "data_inspeksi.json"
image_files = []

state_bucket_inspection = init_state_bucket_inspection()

bucket_data = load_data(DATA_FILE)
bucket_target, bucket_target_snake = load_bucket_inspection_target()

with st.sidebar:
    st.subheader("Gambar1")
    st.subheader("Gambar2")
    st.subheader("Gambar3")

st.title("Inspeksi Bucket")
st.write("Testing")