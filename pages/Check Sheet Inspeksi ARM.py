import streamlit as st
from pathlib import Path
from functions.data_loader import load_data, load_arm_inspection_target
from functions.helper import page_config, init_state_arm_inspection, input_text, input_radio, create_inspection_inputs, process_identities
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
    arm_head_pemeriksaan, arm_head_condition, arm_head_category, arm_head_remark = create_inspection_inputs("Arm Head")
    
    st.subheader("2\\. Welded Side Arm Bottom", help="\n".join(str(i) for i in arm_data['welded_side_arm_bottom'].values()))
    welded_side_arm_bottom_pemeriksaan, welded_side_arm_bottom_condition, welded_side_arm_bottom_category, welded_side_arm_bottom_remark = create_inspection_inputs("Welded Side Arm Bottom")
    
    st.subheader("3\\. Welded Side Arm Head", help="\n".join(str(i) for i in arm_data['welded_side_arm_head'].values()))
    welded_side_arm_head_pemeriksaan, welded_side_arm_head_condition, welded_side_arm_head_category, welded_side_arm_head_remark = create_inspection_inputs("Welded Side Arm Head")
    
    st.subheader("4\\. Boss Pin Arm To Boom", help="\n".join(str(i) for i in arm_data['boss_pin_arm_to_boom'].values()))
    boss_pin_arm_to_boom_pemeriksaan, boss_pin_arm_to_boom_condition, boss_pin_arm_to_boom_category, boss_pin_arm_to_boom_remark = create_inspection_inputs("Boss Pin Arm To Boom")
    
    st.subheader("5\\. Arm Foot", help="\n".join(str(i) for i in arm_data['arm_foot'].values()))
    arm_foot_pemeriksaan, arm_foot_condition, arm_foot_category, arm_foot_remark = create_inspection_inputs("Arm Foot")
    
    st.subheader("6\\. Bracket Link H", help="\n".join(str(i) for i in arm_data['bracket_link_h1'].values()))
    bracket_link_h1_pemeriksaan, bracket_link_h1_condition, bracket_link_h1_category, bracket_link_h1_remark = create_inspection_inputs("Bracket Link H1")
    
    st.subheader("7\\. Bracket Link H", help="\n".join(str(i) for i in arm_data['bracket_link_h2'].values()))
    bracket_link_h2_pemeriksaan, bracket_link_h2_condition, bracket_link_h2_category, bracket_link_h2_remark = create_inspection_inputs("Bracket Link H2")
    
    st.subheader("Mechanic / Welder Comment")
    comment = st.text_area("📝 Masukkan Komentar Setelah Inspeksi!")
    
    submitted = st.form_submit_button("Save")
    
identities = [nama, code_unit, egi, district, hours_meter, 
                date, periode_service, comment]

required_fields = [
    arm_head_pemeriksaan, arm_head_condition, arm_head_category, arm_head_remark,
    welded_side_arm_bottom_pemeriksaan, welded_side_arm_bottom_condition, welded_side_arm_bottom_category, welded_side_arm_bottom_remark,
    welded_side_arm_head_pemeriksaan, welded_side_arm_head_condition, welded_side_arm_head_category, welded_side_arm_head_remark,
    boss_pin_arm_to_boom_pemeriksaan, boss_pin_arm_to_boom_condition, boss_pin_arm_to_boom_category, boss_pin_arm_to_boom_remark,
    arm_foot_pemeriksaan, arm_foot_condition, arm_foot_category, arm_foot_remark,
    bracket_link_h1_pemeriksaan, bracket_link_h1_condition, bracket_link_h1_category, bracket_link_h1_remark,
    bracket_link_h2_pemeriksaan, bracket_link_h2_condition, bracket_link_h2_category, bracket_link_h2_remark
]

if submitted:
    if any((field == 0.0 or field == None or field == "") for field in [*identities, *required_fields]):
        st.error("❌ Ada input yang kosong. Silahkan diisi semuanya!")
        st.stop()
    for target in arm_target:
        if st.session_state.images.get(target) is None:
            st.error("❌ Ada gambar yang belum diambil. Silahkan ambil dokumentasi!")
            st.stop()
    st.session_state.form_submitted = True
    st.session_state.pdf_download = False

if st.session_state.form_submitted:
    identities_processed = process_identities(identities, "inspection")
    
    required_fields_modified = [required_fields[i:i+4] for i in range(0, len(required_fields), 4)]
    temp_dict = dict(zip(arm_target, required_fields_modified))
    
    