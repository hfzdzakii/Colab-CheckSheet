import streamlit as st
import sys, os, io
from pathlib import Path
from PIL import Image
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data_loader import load_bucket_thickness_data, load_bucket_thickness_target
from helper import page_config, init_state_bucket_thickness, input_number, input_radio, reset_confirmation
page_config()

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGES_DIR = BASE_DIR / "images"
image_files = ["Body.png", "Bracket.png", "Get.png"]

# if "form_submitted" not in st.session_state:
#     st.session_state.form_submitted = False
    
# if "open_camera_name" not in st.session_state:
#     st.session_state.open_camera_name = None

# if "warning_images" not in st.session_state:
#     st.session_state.warning_images = {}

# if "warning_notes" not in st.session_state:
#     st.session_state.warning_notes = {}

# if "bad_images" not in st.session_state:
#     st.session_state.bad_images = {}

# if "bad_notes" not in st.session_state:
#     st.session_state.bad_notes = {}

state_bucket_thickness = init_state_bucket_thickness()

bucket_data = load_bucket_thickness_data() # dict
limit = 3
bucket_target, bucket_target_snake = load_bucket_thickness_target() # list

with st.sidebar:
    st.subheader("GET")
    st.image(IMAGES_DIR / image_files[2])
    st.subheader("Body")
    st.image(IMAGES_DIR / image_files[0])
    st.subheader("Bracket")
    st.image(IMAGES_DIR / image_files[1])
    
st.title("Ketebalan Bucket")

with st.form("form_ketebalan_bucket"):
    st.header("GET")
    get1, get2, get3 = st.columns(3)
    with get1:
        bucket_tooth = input_radio("1. Bucket Tooth")
        lock_bucket_tooth = input_radio("2. Lock, Bucket Tooth")
        adapter = input_radio("3. Adapter")
        choky_bar_top = input_number("4. Choky Bar Top / Adapter Top Wear Plate", max=10.0)
    with get2:
        choky_bar_side = input_number("5. Choky Bar Side / Adapter Side Wear Plate", max=10.0)
        lip_shroud = input_radio("6. Lip Shroud / Toplok")
        base_plate = input_number("7. Base Plate / Cutting Edge", max=90.0)
        cutting_edge_top = input_number("8. Cutting Edge Top Wear Plate", max=12.0)
    with get3:
        cutting_edge_bottom = input_number("9. Cutting Edge Bottom Wear Plate", max=16.0)
        wing_shroud = input_radio("10. Wing Shroud")
        heels_shroud = input_radio("11. Heels Shroud")

    submitted = st.form_submit_button("Save")

required_fields = [
    bucket_tooth, lock_bucket_tooth, adapter, choky_bar_top,
    choky_bar_side, lip_shroud, base_plate, cutting_edge_top,
    cutting_edge_bottom, wing_shroud, heels_shroud
]

if submitted:    
    if any((field == "0.00" or field == None) for field in required_fields):
        st.error("❌ Ada input yang kosong. Silahkan diisi semuanya!")
    else:
        st.session_state.form_submitted = True
        st.session_state.open_camera_name = None
        st.session_state.warning_images = {}
        st.session_state.warning_notes = {}
        st.session_state.bad_images = {}
        st.session_state.bad_notes = {}        
    
if st.session_state.form_submitted:
    temp_dict = dict(zip(bucket_target_snake, required_fields))
    check_fields_values = list(bucket_data["GET"].keys()) # int / float
        
    for field_name in check_fields_values:
        if temp_dict[field_name] > bucket_data["GET"][field_name]["min"] + 3:
            temp_dict[field_name] = "👍 Good"
        elif temp_dict[field_name] > bucket_data["GET"][field_name]["min"]:
            temp_dict[field_name] = "⚠️ Warning"
        else:
            temp_dict[field_name] = "❌ Bad"
            
    final_dict = dict(zip(bucket_target, list(temp_dict.values())))
        
    save_flags = [key for key, value in final_dict.items() if value == "👍 Good"]
    
    warning_flags = [key for key, value in final_dict.items() if value == "⚠️ Warning"]
    bad_flags = [key for key, value in final_dict.items() if value == "❌ Bad"]
    
    if not warning_flags and not bad_flags:
        st.success("👍 Semua Aman!")
    
    if warning_flags:
        st.header("⚠️ Warning")
        for idx, name in enumerate(warning_flags):
            st.warning(f"{idx+1}. {name}")
            img_slot = st.empty()
            saved_img = st.session_state.warning_images.get(name)
            if saved_img is not None:
                img_slot.image(saved_img, caption=f"📷 Dokumentasi tersimpan: {name}")
                if st.button("Ambil ulang gambar!", key=f"warning_button_edit_{idx}", icon=":material/camera:"):
                    st.session_state.open_camera_name = name
            else :
                if st.button("Klik untuk membuka Kamera!", key=f"warning_button_{idx}", type="primary", icon=":material/camera:"):
                    st.session_state.open_camera_name = name
            if st.session_state.open_camera_name == name:
                photo = st.camera_input(f"Upload Dokumentasi - {name}!", key=f"warning_cam_{idx}")
                if photo is not None:
                    if st.button("Klik untuk menyimpan foto!", icon=":material/upload:", key=f"warning_upload_{idx}"):
                        image = Image.open(photo)
                        st.session_state.warning_images[name] = image
                        img_slot.image(image, caption=f"📷 Dokumentasi tersimpan: {name}")
                        photo = None
                        st.session_state.open_camera_name = None
                        st.rerun()
            txt = st.text_area("📝 Masukkan Catatan", key=f"warning_note_{idx}")
            st.session_state.warning_notes[name] = txt
        st.divider()
        
    if bad_flags:
        st.header("❌ Bad Condition / Tidak Teridentifikasi / Tidak Ada")
        for idx, name in enumerate(bad_flags):
            st.error(f"{idx+1}. {name}")
            img_slot = st.empty()
            saved_img = st.session_state.bad_images.get(name)
            if saved_img is not None:
                img_slot.image(saved_img, caption=f"📷 Dokumentasi tersimpan: {name}")
                if st.button("Ambil ulang gambar!", key=f"bad_button_edit_{idx}", icon=":material/camera:"):
                    st.session_state.open_camera_name = name
            else:
                if st.button("Klik untuk membuka Kamera!", key=f"bad_button_{idx}", type="primary", icon=":material/camera:"):
                    st.session_state.open_camera_name = name
            if st.session_state.open_camera_name == name:
                photo = st.camera_input(f"Upload Dokumentasi - {name}!", key=f"bad_cam_{idx}")
                if photo is not None:
                    if st.button("Klik untuk menyimpan foto!", icon=":material/upload:", key=f"bad_upload_{idx}"):
                        image = Image.open(photo)
                        st.session_state.bad_images[name] = image
                        img_slot.image(image, caption=f"📷 Dokumentasi tersimpan: {name}")
                        photo = None
                        st.session_state.open_camera_name = None
                        st.rerun()
            txt = st.text_area("Masukkan Catatan", key=f"bad_note_{idx}")
            st.session_state.bad_notes[name] = txt
        st.divider()
    
    if st.button("Reset"):
        reset_confirmation()

    if st.button("Download Laporan PDF (Belum dibuat)"):
        st.text("Belum dibuat. Sabar!")