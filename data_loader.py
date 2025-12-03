import json
from pathlib import Path
import streamlit as st

DATA_PATH = Path(__file__).with_name("data_ketebalan_bucket.json")

@st.cache_data
def load_bucket_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def load_bucket_target():
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
        "Heels Shroud"
    ], [
        "bucket_tooth", "lock_bucket_tooth", "adapter", "choky_bar_top",
        "choky_bar_side", "lip_shroud", "base_plate", "cutting_edge_top",
        "cutting_edge_bottom", "wing_shroud", "heels_shroud"
    ]


def page_config():
    return st.set_page_config(
            page_title="Bucket Parts App",
            layout="wide",
            initial_sidebar_state="expanded",
        )
