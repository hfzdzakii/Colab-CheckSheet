import streamlit as st
import sys, os
from datetime import datetime
from pathlib import Path
from PIL import Image
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data_loader import load_bucket_thickness_data, load_bucket_thickness_target
from helper import page_config, init_state_bucket_thickness, input_number, input_radio, reset_confirmation, create_report_bucket_thickness
page_config()

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGES_DIR = BASE_DIR / "images"
image_files = ["Body.png", "Bracket.png", "Get.png"]

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
    st.header("G.E.T")
    st.subheader("G E T")
    get1, get2, get3 = st.columns(3)
    with get1:
        bucket_tooth = input_radio("1\\. Bucket Toothss")
        lock_bucket_tooth = input_radio("2\\. Lock, Bucket Tooth")
        adapter = input_radio("3\\. Adapter")
        choky_bar_top = input_number("4\\. Choky Bar Top / Adapter Top Wear Plate", help=bucket_data["GET"]["choky_bar_top"])
    with get2:
        choky_bar_side = input_number("5\\. Choky Bar Side / Adapter Side Wear Plate", help=bucket_data["GET"]["choky_bar_side"])
        lip_shroud = input_radio("6\\. Lip Shroud / Toplok")
        base_plate = input_number("7\\. Base Plate / Cutting Edge", help=bucket_data["GET"]["base_plate"])
        cutting_edge_top = input_number("8\\. Cutting Edge Top Wear Plate", help=bucket_data["GET"]["cutting_edge_top"])
    with get3:
        cutting_edge_bottom = input_number("9\\. Cutting Edge Bottom Wear Plate", help=bucket_data["GET"]["cutting_edge_bottom"])
        wing_shroud = input_radio("10\\. Wing Shroud")
        heels_shroud = input_radio("11\\. Heels Shroud")

    # st.space("small")
    
    # st.header("BODY")
    # st.subheader("BODY SKIN")
    # body1, body2 = st.columns(2)
    # with body1:
    #     bucket_skin_inner = input_number("12\\. Bucket Skin Inner Wear Plate", help=bucket_data["BODY_SKIN"]["bucket_skin_inner"])
    #     body_skin_bucket_skin = input_number("13\\. Body Skin / Bucket Skin", help=bucket_data["BODY_SKIN"]["body_skin_bucket_skin"])
    #     bucket_skin_outer_1 = input_number("14\\. Bucket Skin Outer Wear Plate 1", help=bucket_data["BODY_SKIN"]["bucket_skin_outer_1"])
    # with body2:
    #     bucket_skin_outer_2 = input_number("15\\. Bucket Skin Outer Wear Plate 2", help=bucket_data["BODY_SKIN"]["bucket_skin_outer_2"])
    #     outer_frame_1 = input_number("16\\. Outer Frame Wear Plate 1", help=bucket_data["BODY_SKIN"]["outer_frame_1"])
    #     outer_frame_2 = input_number("17\\. Outer Frame Wear Plate 2", help=bucket_data["BODY_SKIN"]["outer_frame_2"])
    # # ---
    # st.subheader("RIGHT SECTION (RH)")
    # rh1, rh2 = st.columns(2)
    # with rh1:
    #     side_wall_rh = input_number("18\\. RH - Side Wall", help=bucket_data["RH"]["side_wall_rh"])
    #     side_wall_inner_rh = input_number("19\\. RH - Side Wall Inner Wear Plate", help=bucket_data["RH"]["side_wall_inner_rh"])
    #     side_wall_outer_1_rh = input_number("20\\. RH - Side Wall Outer Wear Plate 1", help=bucket_data["RH"]["side_wall_outer_1_rh"])
    # with rh2:
    #     side_wall_outer_2_rh = input_number("21\\. RH - Side Wall Outer Wear Plate 2", help=bucket_data["RH"]["side_wall_outer_2_rh"])
    #     side_cutter_rh = input_number("22\\. RH - Side Cutter", help=bucket_data["RH"]["side_cutter_rh"])
    # # ---
    # st.subheader("LEFT SECTION (LH)")
    # lh1, lh2 = st.columns(2)
    # with lh1:
    #     side_wall_lh = input_number("23\\. LH - Side Wall", help=bucket_data["LH"]["side_wall_lh"])
    #     side_wall_inner_lh = input_number("24\\. LH - Side Wall Inner Wear Plate", help=bucket_data["LH"]["side_wall_inner_lh"])
    #     side_wall_outer_1_lh = input_number("25\\. LH - Side Wall Outer Wear Plate 1", help=bucket_data["LH"]["side_wall_outer_1_lh"])
    # with lh2:
    #     side_wall_outer_2_lh = input_number("26\\. LH - Side Wall Outer Wear Plate 2", help=bucket_data["LH"]["side_wall_outer_2_lh"])
    #     side_cutter_lh = input_number("27\\. LH - Side Cutter", help=bucket_data["LH"]["side_cutter_lh"])

    # st.space("small")
    
    # st.header("BRACKET")
    # st.subheader("BRACKET STRUCTURE")
    # plate_bracket = input_radio("28\\. Plate, Bracket Mounting")
    # top_box = input_radio("29\\. Top Box")
    
    submitted = st.form_submit_button("Save")

required_fields = [
    bucket_tooth, lock_bucket_tooth, adapter, choky_bar_top,
    choky_bar_side, lip_shroud, base_plate, cutting_edge_top,
    cutting_edge_bottom, wing_shroud, heels_shroud,
    
    # bucket_skin_inner,body_skin_bucket_skin, bucket_skin_outer_1,
    # bucket_skin_outer_2, outer_frame_1, outer_frame_2,
    
    # side_wall_rh, side_wall_inner_rh, side_wall_outer_1_rh,
    # side_wall_outer_2_rh, side_cutter_rh,
    
    # side_wall_lh, side_wall_inner_lh, side_wall_outer_1_lh,
    # side_wall_outer_2_lh, side_cutter_lh,
    
    # plate_bracket, top_box
]

if submitted:    
    if any((field == 0.00 or field == None) for field in required_fields):
        st.error("❌ Ada input yang kosong. Silahkan diisi semuanya!")
    else:
        st.session_state.form_submitted = True
        st.session_state.pdf_download = False
        st.session_state.open_camera_name = None
        st.session_state.warning_images = {}
        st.session_state.warning_notes = {}
        st.session_state.bad_images = {}
        st.session_state.bad_notes = {}        
    
if st.session_state.form_submitted:
    temp_dict = dict(zip(bucket_target_snake, required_fields))
    
    check_fields_values = [*bucket_data["GET"].keys()] # *bucket_data["BODY_SKIN"].keys(),
                            # *bucket_data["RH"].keys(), *bucket_data["LH"].keys()
    sources = ["GET", "BODY_SKIN", "RH", "LH"]
    
    for field_name in check_fields_values:
        for source in sources:
            field_data = bucket_data.get(source, {}).get(field_name, {})
            if not field_data:
                continue
            min_val = field_data["min"]
            if temp_dict[field_name] > min_val + 3:
                temp_dict[field_name] = "👍 Good"
            elif temp_dict[field_name] > min_val:
                temp_dict[field_name] = "⚠️ Warning"
            else:
                temp_dict[field_name] = "❌ Bad"
            
    final_dict = dict(zip(bucket_target, list(temp_dict.values())))
            
    safe_flags = [key for key, value in final_dict.items() if value == "👍 Good"]
    warning_flags = [key for key, value in final_dict.items() if value == "⚠️ Warning"]
    bad_flags = [key for key, value in final_dict.items() if value == "❌ Bad"]
    missing_images = []
    
    if not warning_flags and not bad_flags:
        st.success("👍 Semua Aman!")
    
    if warning_flags:
        st.header("⚠️ Warning")
        for idx, name in enumerate(warning_flags):
            st.warning(f"{idx+1}. {name}")
            txt = st.text_area(f"📝 Masukkan Catatan untuk {name}", key=f"warning_note_{idx}")
            st.session_state.warning_notes[name] = txt
            img_slot = st.empty()
            saved_img = st.session_state.warning_images.get(name)
            if saved_img is not None:
                img_slot.image(saved_img, caption=f"📷 Dokumentasi tersimpan: {name}")
                if st.button("Ambil ulang gambar!", key=f"warning_button_edit_{idx}", icon=":material/camera:", disabled=False if st.session_state.open_camera_name==None else True):
                    st.session_state.open_camera_name = name
                    st.rerun()
            else :
                if st.button("Klik untuk membuka Kamera!", key=f"warning_button_{idx}", type="primary", icon=":material/camera:", disabled=False if st.session_state.open_camera_name==None else True):
                    st.session_state.open_camera_name = name
                    st.rerun()
            if st.session_state.open_camera_name == name:
                photo = st.camera_input(f"Upload Dokumentasi - {name}!", key=f"warning_cam_{idx}")
                if photo is not None:
                    if st.button("Klik untuk menyimpan foto!", icon=":material/upload:", key=f"warning_upload_{idx}", type="primary"):
                        try:
                            image = Image.open(photo)
                            st.session_state.warning_images[name] = image
                            img_slot.image(image, caption=f"📷 Dokumentasi tersimpan: {name}")
                            photo = None
                            st.session_state.open_camera_name = None
                            st.rerun()
                            st.toast("✔️ Foto berhasil diupload!")
                        except Exception as e:
                            st.toast(f"❌ Error : {e}")
        st.divider()
        
    if bad_flags:
        st.header("❌ Bad Condition / Tidak Teridentifikasi / Tidak Ada")
        for idx, name in enumerate(bad_flags):
            st.error(f"{idx+1}. {name}")
            txt = st.text_area(f"📝 Masukkan Catatan untuk {name}", key=f"bad_note_{idx}")
            st.session_state.bad_notes[name] = txt
            img_slot = st.empty()
            saved_img = st.session_state.bad_images.get(name)
            if saved_img is not None:
                img_slot.image(saved_img, caption=f"📷 Dokumentasi tersimpan: {name}")
                if st.button("Ambil ulang gambar!", key=f"bad_button_edit_{idx}", icon=":material/camera:", disabled=False if st.session_state.open_camera_name==None else True):
                    st.session_state.open_camera_name = name
                    st.rerun()
            else:
                if st.button("Klik untuk membuka Kamera!", key=f"bad_button_{idx}", type="primary", icon=":material/camera:", disabled=False if st.session_state.open_camera_name==None else True):
                    st.session_state.open_camera_name = name
                    st.rerun()
            if st.session_state.open_camera_name == name:
                photo = st.camera_input(f"Upload Dokumentasi - {name}!", key=f"bad_cam_{idx}")
                if photo is not None:
                    if st.button("Klik untuk menyimpan foto!", icon=":material/upload:", key=f"bad_upload_{idx}", type="primary"):
                        try:
                            image = Image.open(photo)
                            st.session_state.bad_images[name] = image
                            img_slot.image(image, caption=f"📷 Dokumentasi tersimpan: {name}")
                            photo = None
                            st.session_state.open_camera_name = None
                            st.toast("✔️ Foto berhasil diupload!")
                            st.rerun()
                        except Exception as e:
                            st.toast(f"❌ Error : {e}")
        st.divider()
    
    if st.button("Reset"):
        reset_confirmation()

    if st.button("📄 Download Laporan PDF!", disabled=False if st.session_state.open_camera_name==None else True):
        st.session_state.pdf_download = True
        
    if st.session_state.pdf_download:
        missing_notes = []
        missing_images = []
        
        for idx, name in enumerate(warning_flags):
            warning_note_key = f"warning_note_{idx}"
            warning_cam_key = f"warning_cam_{idx}"
            if st.session_state.get(warning_note_key) == "":
                missing_notes.append(name)
            if st.session_state.get(warning_cam_key) is None:
                missing_images.append(name)

        for idx, name in enumerate(bad_flags):
            bad_note_key = f"bad_note_{idx}"
            bad_cam_key = f"bad_cam_{idx}"
            if st.session_state.get(bad_note_key) == "":
                missing_notes.append(name)
            if st.session_state.get(bad_cam_key) is None:
                missing_images.append(name)
        
        if missing_notes:
            st.error("❌ Catatan wajib diisi untuk item berikut:")
            for i, name in enumerate(missing_notes, start=1):
                st.write(f"{i}. {name}")
        st.space("small")
        if missing_images:
            st.error("❌ Dokumentasi Gambar wajib diisi untuk item berikut:")
            for i, name in enumerate(missing_images, start=1):
                st.write(f"{i}. {name}")
            st.stop()
        else:
            pdf_buffer = create_report_bucket_thickness(dict(zip(bucket_target, required_fields)), 
                                                        safe_flags, warning_flags, bad_flags, 
                                                        st.session_state.warning_images,
                                                        st.session_state.bad_images,
                                                        st.session_state.warning_notes,
                                                        st.session_state.bad_notes)
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            st.download_button("Download PDF", pdf_buffer, file_name=f"Report_Ketebalan_Bucket_{timestamp}.pdf", mime="application/pdf", icon=":material/download:", disabled=False if st.session_state.open_camera_name==None else True)
        
        