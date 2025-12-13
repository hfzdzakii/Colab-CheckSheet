import streamlit as st
import time
import tempfile
from dataclasses import dataclass, field
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
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
    pdf_download:bool = False
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
        pdf_download=st.session_state.pdf_download,
        open_camera_name=st.session_state.open_camera_name,
        warning_images=st.session_state.warning_images,
        warning_notes=st.session_state.warning_notes,
        bad_images=st.session_state.bad_images,
        bad_notes=st.session_state.bad_notes,
    )

def input_radio(message, options=["👍 Good", "❌ Bad"]):
    return st.radio(message, options, horizontal=True, index=None)

def input_number(message, help):
    return st.number_input(message, max_value=help["std"], min_value=0.0, format="%.2f", placeholder="Gunakan titik (.) sebagai pengganti koma (,)", help=f"std:{help["std"]}, min:{help["min"]}", value=None)

def input_text(message):
    return st.text_input(message, value=None)

@st.dialog("Yakin melakukan Reset?")
def reset_confirmation():
    st.write("Melakukan reset akan menghilangkan semua data.")
    with st.spinner("Tunggu..."):
        time.sleep(3)
    if st.button("Reset!", type="primary", icon=":material/delete:", width="stretch"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
        
def process_identities(identities):
    nama_processed = f"Nama: {identities[0]}"
    nrp_processed = f"NRP: {identities[1]}"
    jabatan_processed = f"Jabatan: {identities[2]}"
    district_processed = f"District: {identities[3]}"
    date_processed = f"Tanggal Insp: {identities[4]}"
    egi_processed = f"EGI: {identities[5]}"
    hm_unit_processed = f"HM Unit: {identities[6]}"
    ps_processed = f"PS: {identities[7]}"
    metode_insp_processed = f"Metode Insp: {identities[8]}"
    return [nama_processed, nrp_processed, jabatan_processed,
            district_processed, date_processed, egi_processed,
            hm_unit_processed, ps_processed, metode_insp_processed]
                                                # targets : zip(bucket_target, required_fields)
def create_report_bucket_thickness(identities, targets_and_data, s_flags, w_flags, b_flags, w_imgs, b_imgs, w_notes, b_notes): # flag : list | notes : dict
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    elements = []
    
    hanging_style = ParagraphStyle(
        name="HangingNumber",
        parent=styles["Normal"],
        leftIndent=30,
        firstLineIndent=-20
    )
    
    elements.append(Paragraph("Laporan Ketebalan Bucket", styles["Title"]))
    elements.append(Spacer(1, 20))
    
    MAX_WIDTH = 300
    
    if len(w_flags) == 0 and len(b_flags) == 0:
        # Safe Section
        elements.append(Paragraph("List part yang aman :", styles["Normal"]))
        elements.append(Spacer(1, 10))
        for idx, safe in enumerate(s_flags):
            elements.append(Paragraph(f"{idx+1}. {safe}", hanging_style))
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(f"Status / Ketebalan (mm) : {targets_and_data[safe]}", hanging_style))
            elements.append(Spacer(1, 8))
    else:
        # Safe Section
        elements.append(Paragraph("List part yang aman :", styles["Normal"]))
        elements.append(Spacer(1, 10))
        for idx, safe in enumerate(s_flags):
            elements.append(Paragraph(f"{idx+1}. {safe}", hanging_style))
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(f"Status / Ketebalan (mm) : {targets_and_data[safe]}", hanging_style))
            elements.append(Spacer(1, 8))
            
        elements.append(Spacer(1, 12))
        
        # Warning Section
        elements.append(Paragraph("List part yang Warning :", styles["Normal"]))
        elements.append(Spacer(1, 10))
        for idx, warning in enumerate(w_flags):
            elements.append(Paragraph(f"{idx+1}. {warning}", hanging_style))
            elements.append(Spacer(1, 5))
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            w_imgs[warning].save(tmp.name)
            orig_w, orig_h = w_imgs[warning].size
            scale = MAX_WIDTH / orig_w
            pdf_h = orig_h * scale
            elements.append(RLImage(tmp.name, width=MAX_WIDTH, height=pdf_h))
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(f"Status / Ketebalan (mm) : {targets_and_data[warning]}", hanging_style))
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(f"Catatan : {w_notes[warning]}", hanging_style))
            elements.append(Spacer(1, 8))
            
        elements.append(Spacer(1, 12))
        
        # Bad Section
        elements.append(Paragraph("List part yang Bad / Tidak Teridentifikasi / Tidak Ada :", styles["Normal"]))
        elements.append(Spacer(1, 10))
        for idx, bad in enumerate(b_flags):
            elements.append(Paragraph(f"{idx+1}. {bad}", hanging_style))
            elements.append(Spacer(1, 5))
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            b_imgs[bad].save(tmp.name)
            orig_w, orig_h = b_imgs[bad].size
            scale = MAX_WIDTH / orig_w
            pdf_h = orig_h * scale
            elements.append(RLImage(tmp.name, width=MAX_WIDTH, height=pdf_h))
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(f"Status / Ketebalan (mm) : {targets_and_data[bad]}", hanging_style))
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(f"Catatan : {b_notes[bad]}", hanging_style))
            elements.append(Spacer(1, 8))
            
    doc.build(elements)
    
    buffer.seek(0)
    return buffer