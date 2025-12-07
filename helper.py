import streamlit as st
from dataclasses import dataclass, field
import time

def page_config():
    return st.set_page_config(
            page_title="Bucket Parts App",
            layout="wide",
            initial_sidebar_state="expanded",
        )
    
@dataclass
class AppStateBucketThickness:
    form_submitted: bool = False
    open_camera_name: str | None = None
    warning_images:dict = field(default_factory=dict)
    warning_notes:dict = field(default_factory=dict)
    bad_images:dict = field(default_factory=dict)
    bad_notes:dict = field(default_factory=dict)
    
def init_state_bucket_thickness() -> AppStateBucketThickness:
    for key, default in AppStateBucketThickness().__dict__.items():
        st.session_state.setdefault(key, default)
    return AppStateBucketThickness(
        form_submitted=st.session_state.form_submitted,
        open_camera_name=st.session_state.open_camera_name,
        warning_images=st.session_state.warning_images,
        warning_notes=st.session_state.warning_notes,
        bad_images=st.session_state.bad_images,
        bad_notes=st.session_state.bad_notes,
    )

def input_radio(message, options=["👍 Good", "❌ Bad"]):
    return st.radio(message, options, horizontal=True, index=None)

def input_number(message, max):
    return st.number_input(message, max_value=max, min_value=0.0, format="%.2f", help="Gunakan titik (.) sebagai pengganti koma.")

@st.dialog("Konfirmasi Reset?")
def reset_confirmation():
    st.subheader("Yakin melakukan Reset?")
    st.write("Melakukan reset akan menghilangkan semua data.")
    with st.spinner("Tunggu 5 detik...", show_time=True):
        time.sleep(5)
    if st.button("Reset!", type="primary", icon=":material/delete:", width="stretch"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()