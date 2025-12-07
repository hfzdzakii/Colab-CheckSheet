import streamlit as st
import time
import tempfile
from dataclasses import dataclass, field
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

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

@st.dialog("Yakin melakukan Reset?")
def reset_confirmation():
    st.write("Melakukan reset akan menghilangkan semua data.")
    with st.spinner("Tunggu 3 detik...", show_time=True):
        time.sleep(3)
    if st.button("Reset!", type="primary", icon=":material/delete:", width="stretch"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
        
def create_report_bucket_thickness(s_flags, w_flags, b_flags, w_imgs, b_imgs, w_notes, b_notes):
    if len(w_flags) == 0 and len(b_flags) == 0:
        pass # Show semua Safe Flags
    else:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        
        elements.append(Paragraph("Laporan Ketebalan Bucket", styles["Title"]))
        elements.append(Spacer(1, 20))