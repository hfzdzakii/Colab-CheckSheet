import streamlit as st
from pathlib import Path
from functions.data_loader import load_data, load_arm_inspection_target
from functions.helper import page_config, init_state_arm_inspection, input_text, input_radio, create_inspection_inputs2, process_identities, reset_confirmation
page_config()

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = None
DATA_FILE = BASE_DIR / "data" / "data_inspeksi.json"
image_files = []

arm_data = load_data(DATA_FILE)["ARM"]
arm_target, arm_target_snake = load_arm_inspection_target()
state_arm_inspection = init_state_arm_inspection(arm_target)

with st.sidebar:
    st.subheader("Gambar1")
    st.subheader("Gambar2")
    st.subheader("Gambar3")

st.title("Inspeksi ARM")

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
# ====
for idx, (target, target_snake) in enumerate(list(zip(arm_target, arm_target_snake))[:2], start=1):
    st.subheader(f"{idx}\\. {target}", help="\n".join(str(i) for i in arm_data[target_snake].values()))
    create_inspection_inputs2(target, target_snake)
# ====
st.subheader("Mechanic / Welder Comment")
comment = st.text_area("📝 Masukkan Komentar Setelah Inspeksi!")
    
submitted = st.button("Save")
    
#  ===============================    
identities = [nama, code_unit, egi, district, hours_meter, 
                date, periode_service, comment]

# if submitted:
#     if any((field == 0.0 or field == None or field == "") for field in [*identities, *required_fields]):
#         st.error("❌ Ada input yang kosong. Silahkan diisi semuanya!")
#         st.stop()
#     for target in arm_target:
#         if st.session_state.images.get(target) is None:
#             st.error("❌ Ada gambar yang belum diambil. Silahkan ambil dokumentasi!")
#             st.stop()
#     st.session_state.form_submitted = True
#     st.session_state.pdf_download = False

# if st.session_state.form_submitted:
#     identities_processed = process_identities(identities, "inspection")
    
#     required_fields_modified = [required_fields[i:i+4] for i in range(0, len(required_fields), 4)]
#     final_dict = dict(zip(arm_target, required_fields_modified))
    
    