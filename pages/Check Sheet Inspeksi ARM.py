import streamlit as st
from pathlib import Path
from functions.data_loader import load_data, load_arm_inspection_target
from functions.helper import page_config, init_state_arm_inspection, input_text, input_radio, create_inspection_inputs
page_config()

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = None
DATA_FILE = BASE_DIR / "data" / "data_inspeksi.json"
image_files = []

state_arm_inspection = init_state_arm_inspection()

arm_data = load_data(DATA_FILE)["ARM"]
arm_target, arm_target_snake = load_arm_inspection_target()

with st.sidebar:
    st.subheader("Gambar1")
    st.subheader("Gambar2")
    st.subheader("Gambar3")

st.title("Inspeksi ARM")

with st.form("form_inspeksi_arm"):
    st.header("Identitas")
    id1, id2 = st.columns(2)
    with id1:
        nama = input_text("Nama")
        code_unit = input_text("Code Unit")
        egi = input_text("EGI")
        district = input_text("District")
    with id2:
        hours_meter = input_text("Hours Meter")
        date = st.date_input("Tanggal Insp", value="today", disabled=True, format="DD/MM/YYYY", help="Otomatis terisi hari ini!")
        periode_service = input_radio("Periode Service", "periode")
        
    st.space("small")
        
    st.header("NDT ARM")
    
    st.subheader("1\\. Arm Head", help="\n".join(str(i) for i in arm_data['arm_head'].values()))
    arm_head_pemeriksaan, arm_head_condition, arm_head_category, arm_head_remark = create_inspection_inputs()
    
    