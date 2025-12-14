import streamlit as st
from pathlib import Path
from functions.data_loader import load_data
from functions.helper import page_config, init_state_arm_inspection
page_config()

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = None
DATA_FILE = BASE_DIR / "data" / "data_inspeksi_arm.json"
image_files = []

state_arm_inspection = init_state_arm_inspection()

arm_data = load_data(DATA_FILE)
arm_target, arm_target_snake ={}

with st.sidebar:
    st.subheader("Gambar1")
    st.subheader("Gambar2")
    st.subheader("Gambar3")

st.title("Inspeksi ARM")

with st.form("form_inspeksi_arm"):
    pass