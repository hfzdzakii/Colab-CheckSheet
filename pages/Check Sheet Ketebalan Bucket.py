import streamlit as st
import sys, os
import pandas as pd
from PIL import Image
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data_loader import page_config, load_bucket_data, load_bucket_target
page_config()

bucket_data = load_bucket_data() # dict
limit = 3
bucket_target, bucket_target_snake = load_bucket_target() # list

def create_doc(val):
    if isinstance(val, str):
        return "String"
    elif isinstance(val, int):
        return "Integer"
    elif isinstance(val, float):
        return "Float"
    else:
        return "Not all"


st.title("Ketebalan Bucket")

with st.form("form_ketebalan_bucket"):
    st.header("GET")
    get1, get2, get3 = st.columns(3)
    with get1:
        bucket_tooth = st.radio("Bucket Tooth", ["👍 Good", "❌ Bad"], horizontal=True, index=None)
        lock_bucket_tooth = st.radio("Lock, Bucket Tooth", ["👍 Good", "❌ Bad"], horizontal=True, index=None)
        adapter = st.radio("Adapter", ["👍 Good", "❌ Bad"], horizontal=True, index=None)
        choky_bar_top = st.number_input("Choky Bar Top / Adapter Top Wear Plate", max_value=10, min_value=0)
    with get2:
        choky_bar_side = st.number_input("Choky Bar Side / Adapter Side Wear Plate", max_value=10, min_value=0)
        lip_shroud = st.radio("Lip Shroud / Toplok", ["👍 Good", "❌ Bad"], horizontal=True, index=None)
        base_plate = st.number_input("Base Plate / Cutting Edge", max_value=90, min_value=0)
        cutting_edge_top = st.number_input("Cutting Edge Top Wear Plate", max_value=12, min_value=0)
    with get3:
        cutting_edge_bottom = st.number_input("Cutting Edge Bottom Wear Plate", max_value=16, min_value=0)
        wing_shroud = st.radio("Wing Shroud", ["👍 Good", "❌ Bad"], horizontal=True, index=None)
        heels_shroud = st.radio("Heels Shroud", ["👍 Good", "❌ Bad"], horizontal=True, index=None)

    submitted = st.form_submit_button("Save")

if submitted:
    required_fields = [
        bucket_tooth, lock_bucket_tooth, adapter, choky_bar_top,
        choky_bar_side, lip_shroud, base_plate, cutting_edge_top,
        cutting_edge_bottom, wing_shroud, heels_shroud
    ]
    
    if any((field == "0" or field == None) for field in required_fields):
        st.error("❌ Ada input yang kosong. Silahkan diisi semuanya!")
    else:
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
        warning_images = []
        
        bad_flags = [key for key, value in final_dict.items() if value == "❌ Bad"]
        bad_images = []
        
        if not warning_flags and not bad_flags:
            st.success("All Success!")
        
        if warning_flags:
            st.header("Warning")
            for idx, name in enumerate(warning_flags):
                st.warning(f"""{idx+1}. {name}""")
                photo = st.camera_input(f"Upload Dokumentasi - {name}!", key=f"cam_{idx}")
                if photo is not None:
                    image = Image.open(photo)
                    warning_images.append(image)
                    st.image(image, caption="Captured Image", use_container_width=True)
                    st.success("✅ Photo captured successfully!")
            st.divider()
            
        if bad_flags:
            st.header("Bad Condition / Tidak Teridentifikasi / Tidak Ada")
            for idx, name in enumerate(bad_flags):
                st.error(f"""{idx+1}. {name}""")
                photo = st.camera_input(f"Upload Dokumentasi - {name}!", key=f"cam_{idx}")
                if photo is not None:
                    image = Image.open(photo)
                    warning_images.append(image)
                    st.image(image, caption="Captured Image", use_container_width=True)
                    st.success("✅ Photo captured successfully!")
            st.divider()
        
        
        st.button("Download Laporan PDF (Belum dibuat)")
        
