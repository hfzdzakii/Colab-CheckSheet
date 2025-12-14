import streamlit as st
import sys, os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from helper import page_config, init_state_bucket_inspection
page_config()

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = None
image_files = []

state_bucket_inspection = init_state_bucket_inspection()

with st.sidebar:
    st.subheader("Gambar1")
    st.subheader("Gambar2")
    st.subheader("Gambar3")

st.title("Inspeksi Bucket")
st.write("Testing")