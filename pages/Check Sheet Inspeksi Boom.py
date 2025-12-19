import streamlit as st
from pathlib import Path
from functions.check_sheet_inspeksi_template import inspection_template
from functions.data_loader import load_data, load_boom_inspection_target
from functions.helper import page_config, init_state_inspection
page_config()

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = None
DATA_FILE = BASE_DIR / "data" / "data_inspeksi.json"
PART_NAME = "Boom" # <== change this

data = load_data(DATA_FILE)[PART_NAME]
target, target_snake = load_boom_inspection_target() # <== change this
state_inspection = init_state_inspection(target)

with st.sidebar:
    st.subheader("Gambar1")
    st.subheader("Gambar2")
    st.subheader("Gambar3")
    
inspection_template(PART_NAME, data, target, target_snake)