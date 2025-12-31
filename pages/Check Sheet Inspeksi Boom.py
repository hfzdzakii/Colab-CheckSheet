import streamlit as st
from pathlib import Path
from functions.check_sheet_inspeksi_template import inspection_template
from functions.data_loader import load_data, load_boom_inspection_target
from functions.helper import page_config, init_state_inspection

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = BASE_DIR / "images"
DATA_FILE = BASE_DIR / "data" / "data_inspeksi.json"
PART_NAME = "Boom" # <== change this
image_files = [f"NDT_{PART_NAME}_{i}.png" for i in range(1, 3)]

data = load_data(DATA_FILE)[PART_NAME]
target, target_snake = load_boom_inspection_target() # <== change this
state_inspection = init_state_inspection(PART_NAME, target)

page_config(PART_NAME)

with st.sidebar:
    st.subheader(f"{PART_NAME}")
    for i in image_files:
        st.image(IMAGE_DIR / i)
    
inspection_template(PART_NAME, data, target, target_snake)