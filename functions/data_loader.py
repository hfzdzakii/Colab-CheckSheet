import json
from pathlib import Path
import streamlit as st

@st.cache_data
def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
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

def load_arm_inspection_target():
    return [
        "Arm Head",
        "Welded Side Arm Bottom",
        # "Welded Side Arm Head",
        # "Boss Pin Arm To Boom",
        # "Arm Foot",
        # "Bracket Link H1",
        # "Bracket Link H2"
    ], [
        "arm_head",
        "welded_side_arm_bottom",
        # "welded_side_arm_head",
        # "boss_pin_arm_to_boom",
        # "arm_foot",
        # "bracket_link_h1",
        # "bracket_link_h2"
    ]

def load_boom_inspection_target():
    return [
        "Boom Head",
        "Body Boom Top",
        "Bracket Of Bottom Arm Cyl",
        "Body Boom Bottom",
        "Boom Foot"
    ], [
        "boom_head",
        "body_boom_top",
        "bracket_of_bottom_arm_cyl",
        "body_boom_bottom",
        "boom_foot"
    ]

def load_bucket_inspection_target():
    return [
        "Heel Shroud",
        "Side Cutters",
        "Kupingan Bucket & Area Pin",
        "Welding Base Plate LH/RH",
        "Lip Shroud",
        "Adaptor Bucket"
    ], [
        "heel_shroud",
        "side_cutters",
        "kupingan_bucket_and_area_pin",
        "welding_base_plate_lh_rh",
        "lip_shroud",
        "adaptor_bucket"
    ]
