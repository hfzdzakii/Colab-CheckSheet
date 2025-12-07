import json
from pathlib import Path
import streamlit as st

DATA_PATH = Path(__file__).with_name("data_ketebalan_bucket.json")

@st.cache_data
def load_bucket_thickness_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def load_bucket_thickness_target():
    return [
        "Bucket Tooth",
        "Lock, Bucket Tooth",
        "Adapter",
        "Choky Bar Top / Adapter Top Wear Plate",
        "Choky Bar Side / Adapter Side Wear Plate",
        "Lip Shroud / Toplok",
        "Base Plate / Cutting Edge",
        "Cutting Edge Top Wear Plate",
        "Cutting Edge Bottom Wear Plate",
        "Wing Shroud",
        "Heels Shroud",
        
        "Bucket Skin Inner Wear Plate",
        "Body Skin / Bucket Skin",
        "Bucket Skin Outer Wear Plate 1",
        "Bucket Skin Outer Wear Plate 2",
        "Outer Frame Wear Plate 1",
        "Outer Frame Wear Plate 2",
        
        "RH - Side Wall",
        "RH - Side Wall Inner Wear Plate",
        "RH - Side Wall Outer Wear Plate 1",
        "RH - Side Wall Outer Wear Plate 2",
        "RH - Side Cutter",
        
        "LH - Side Wall",
        "LH - Side Wall Inner Wear Plate",
        "LH - Side Wall Outer Wear Plate 1",
        "LH - Side Wall Outer Wear Plate 2",
        "LH - Side Cutter",
        
        "Plate, Bracket Mounting",
        "Top Box"
    ], [
        "bucket_tooth", "lock_bucket_tooth", "adapter", "choky_bar_top",
        "choky_bar_side", "lip_shroud", "base_plate", "cutting_edge_top",
        "cutting_edge_bottom", "wing_shroud", "heels_shroud",
        
        "bucket_skin_inner", "body_skin_bucket_skin", "bucket_skin_outer_1",
        "bucket_skin_outer_2", "outer_frame_1", "outer_frame_2",
        
        "side_wall_rh", "side_wall_inner_rh", "side_wall_outer_1_rh",
        "side_wall_outer_2_rh", "side_cutter_rh",
        
        "side_wall_lh", "side_wall_inner_lh", "side_wall_outer_1_lh",
        "side_wall_outer_2_lh", "side_cutter_lh",
        
        "plate_bracket", "top_box"
    ]
