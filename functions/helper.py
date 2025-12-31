import streamlit as st
import time
import base64
from pathlib import Path
import tempfile
from PIL import Image
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

BASE_DIR = Path(__file__).resolve().parents[1]
FONT_PATH = BASE_DIR / "fonts/BRLNSDB.TTF"
FONT_NAME = 'Berlin Sans FB Demi'

def delete_session_some(PART):
    for key in st.session_state.keys():
        if str(key).startswith(PART):
            continue
        del st.session_state[key]

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def nav_and_back():
    st.page_link("Welcome.py", label="🏠 Kembali")

def page_config(PART, font_path=FONT_PATH, font_name=FONT_NAME):
    with open(font_path, "rb") as f:
        encoded_font = base64.b64encode(f.read()).decode()
    
    st.markdown(
        f"""
        <style>
        @font-face {{
            font-family: '{font_name}';
            src: url(data:font/ttf;base64,{encoded_font}) format('truetype');
            font-weight: normal;
            font-style: normal;
        }}

        html, body, .stApp {{
            font-family: '{font_name}', sans-serif !important;
        }}
        
        h1, h2, h3, h4, h5, h6,
        p, label, li, a, div {{
            font-family: '{font_name}', sans-serif !important;
        }}
        
        input, textarea, select {{
            font-family: '{font_name}', sans-serif !important;
        }}
        
        button {{
            font-family: '{font_name}', sans-serif !important;
        }}
        [class*="css-"] {{
            font-family: '{font_name}', sans-serif !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.set_page_config(
        page_title="Bucket Parts App",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    delete_session_some(PART) # <=======================================
    
@dataclass
class AppStateBucketThickness:
    form_submitted: bool = False
    pdf_download:bool = False
    open_camera_name: str | None = None
    warning_images:dict = field(default_factory=dict)
    warning_notes:dict = field(default_factory=dict)
    bad_images:dict = field(default_factory=dict)
    bad_notes:dict = field(default_factory=dict)
    
def init_state_bucket_thickness(PART) -> AppStateBucketThickness:
    for key, default in AppStateBucketThickness().__dict__.items():
        st.session_state.setdefault(f"{PART}_{key}", default)
    return AppStateBucketThickness(
        form_submitted=st.session_state[f"{PART}_form_submitted"],
        pdf_download=st.session_state[f"{PART}_pdf_download"],
        open_camera_name=st.session_state[f"{PART}_open_camera_name"],
        warning_images=st.session_state[f"{PART}_warning_images"],
        warning_notes=st.session_state[f"{PART}_warning_notes"],
        bad_images=st.session_state[f"{PART}_bad_images"],
        bad_notes=st.session_state[f"{PART}_bad_notes"]
    )
    
@dataclass
class AppStateInspection:
    submitted: bool = False
    pdf_download:bool = False
    open_camera_name: str | None = None
    images: dict = field(default_factory=dict)
    data: dict = field(default_factory=dict)

def init_state_inspection(PART: str, targets:list) -> AppStateInspection:
    st.session_state.setdefault(f"{PART}_submitted", False)
    st.session_state.setdefault(f"{PART}_pdf_download", False)
    st.session_state.setdefault(f"{PART}_open_camera_name", None)
    st.session_state.setdefault(f"{PART}_images", {})
    st.session_state.setdefault(f"{PART}_data", {})
    for target in targets:
        st.session_state[f"{PART}_data"].setdefault(
            target,
            {
                "pemeriksaan": None,
                "condition": None,
                "category": None,
                "remark": None,
            }
        )
    return AppStateInspection(
        submitted=st.session_state[f"{PART}_submitted"],
        pdf_download=st.session_state[f"{PART}_pdf_download"],
        open_camera_name=st.session_state[f"{PART}_open_camera_name"],
        images=st.session_state[f"{PART}_images"],
        data=st.session_state[f"{PART}_data"],
    )

def input_radio(message, option):
    if option == "thickness":
        options = ["👍 Good", "❌ Bad"]
    if option == "periode":
        options = ["PS 1", "PS 2", "PS 3", "PS 4"]
    return st.radio(message, options, horizontal=True, index=None)

def input_multiselect(message, option, key):
    if option == "pemeriksaan":
        options = ["⚡ Ultrasonic Test ✨", "💧 Penetrant Test 🔍", "👀 Visual Test 🔍"]
    return st.multiselect(message, options, default=[], key=key)

def input_selectbox(message, option, key):
    if option == "condition":
        options = ["-", "✅ Good Condition 👍", "❌ Bad Condition ⚠️", "🛠️ Sudah Repair Hasil Baik ✅", "🔁🛠️ Sudah Repair, Repair Ulang (REDO) ⚠️"]
    if option == "category":
        options = ["-", "🚨 Action Sekarang Juga ⚡", "⏳ Action < 72 Jam ⏰", "📅 Action saat Service selanjutnya 🔧", "🛠️ Action saat Overhaul (General Repair) 🏗️"]
    if option == "remark":
        options = ["-", "❓ LOST", "💥 CRACK", "⚙️ WEAR", "🔨 DAMAGE", "✅ NO DEFECT"]
    return st.selectbox(message, options, key=key)

def input_number(message, help):
    return st.number_input(message, max_value=help["std"], min_value=0.0, format="%.2f", placeholder="Gunakan titik (.)", help=f"std:{help["std"]}, min:{help["min"]}", value=None)

def input_text(message):
    return st.text_input(message, value=None)

def create_inspection_inputs(PART, name_snake):
    col1, col2 = st.columns(2)
    with col1:
        input_multiselect("Jenis Pemeriksaan", "pemeriksaan", f"{PART}_{name_snake}_pemeriksaan")
        input_selectbox("Jenis Kondisi", "condition", f"{PART}_{name_snake}_condition")
    with col2:
        input_selectbox("Kategori", "category", f"{PART}_{name_snake}_category")
        input_selectbox("Remark", "remark", f"{PART}_{name_snake}_remark")
    img_slot = st.empty()
    saved_img = st.session_state[f"{PART}_images"].get(f"{PART}_{name_snake}_gambar")
    if saved_img is not None:
        img_slot.image(saved_img, caption=f"📷 Dokumentasi tersimpan: {name_snake.replace("_", " ").title()}", width=200)
        if st.button("Ambil ulang gambar!", key=f"{PART}_{name_snake}_retake_image_button", icon=":material/camera:", disabled=False if st.session_state[f"{PART}_open_camera_name"]==None else True):
            st.session_state[f"{PART}_open_camera_name"] = name_snake
            st.rerun()
    else :
        if st.button("Klik untuk membuka Kamera!", key=f"{PART}_{name_snake}_open_cam_button", type="primary", icon=":material/camera:", disabled=False if st.session_state[f"{PART}_open_camera_name"]==None else True):
            st.session_state[f"{PART}_open_camera_name"] = name_snake
            st.rerun()
    if st.session_state[f"{PART}_open_camera_name"] == name_snake:
        photo = st.camera_input(f"Upload Dokumentasi - {name_snake.replace("_", " ").title()}!")
        if photo is not None:
            if st.button("Klik untuk menyimpan foto!", key=f"{PART}_{name_snake}_safe_image_button", icon=":material/upload:", type="primary"):
                try:
                    image = Image.open(photo)
                    st.session_state[f"{PART}_images"][f"{PART}_{name_snake}_gambar"] = image
                    img_slot.image(image, caption=f"📷 Dokumentasi tersimpan: {name_snake.replace("_", " ").title()}", width=200)
                    photo = None
                    st.session_state[f"{PART}_open_camera_name"] = None
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error : {e}")
            
def apply_data_inspection(PART, names, names_snake):
    for name, name_snake in list(zip(names, names_snake)):
        st.session_state[f"{PART}_data"][name] = {
            "pemeriksaan": st.session_state[f"{PART}_{name_snake}_pemeriksaan"],
            "condition": st.session_state[f"{PART}_{name_snake}_condition"],
            "category": st.session_state[f"{PART}_{name_snake}_category"],
            "remark": st.session_state[f"{PART}_{name_snake}_remark"],
        }
        
@st.dialog("Download Laporan", dismissible=False)
def pdf_dialog(PART, pdf_buffer, file_name):
    st.write("PDF siap diunduh!")
    st.download_button(
        "Download PDF",
        pdf_buffer,
        file_name,
        mime="application/pdf",
        icon=":material/download:",
        width="stretch",
        type="primary"
    )
    if st.button("Tutup", width="stretch"):
        st.session_state[f"{PART}_pdf_download"] = False
        st.rerun()
        
def process_identities(identities, mode):
    if mode == "thickness":
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
    if mode == "inspection":
        nama_processed = f"Nama: {identities[0]}"
        code_unit_processed = f"Code Unit: {identities[1]}"
        egi_processed = f"EGI: {identities[2]}"
        district_processed = f"District: {identities[3]}"
        hours_meter_processed = f"Hours Meter: {identities[4]}"
        date_processed = f"Tanggal Insp: {identities[5]}"
        periode_service_processed = f"Periode Service: {identities[6]}"
        comment = identities[7]
        return [nama_processed, code_unit_processed, egi_processed,
                district_processed, hours_meter_processed, date_processed,
                periode_service_processed, comment]

                                                # targets : zip(bucket_target, required_fields)
def create_report_bucket_thickness(identities, targets_and_data, s_flags, w_flags, b_flags, w_imgs, b_imgs, w_notes, b_notes): # flag : list | notes : dict
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    elements = []
    
    title_style = styles["Title"]
    elements.append(Paragraph("Laporan Ketebalan Bucket", title_style))
    elements.append(Spacer(1, 12))
    
    ids = (identities + [""] * 9)[:9]
    table_data = [ids[i:i+3] for i in range(0, 9, 3)]
    
    table_style = TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ])
    
    identity_table = Table(table_data, colWidths=[doc.width / 3] * 3)
    identity_table.setStyle(table_style)
    elements.append(identity_table)
    elements.append(Spacer(1, 12))
    MAX_IMG_HEIGHT = 7.5 * cm
    
    bold_sub = ParagraphStyle(
        name="BoldSub",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        spaceAfter=6
    )
    
    # Safe Section
    if s_flags:
        elements.append(Paragraph("List Part Safe!", bold_sub))
        elements.append(Spacer(1, 6))
        for i, safe in enumerate(s_flags, start=1):
            elements.append(Paragraph(f"{i}. {safe}", styles["Normal"]))
            elements.append(Spacer(1, 2))
            elements.append(Paragraph(f"Status / Ketebalan (mm): {targets_and_data[safe]}", styles["Normal"]))
            elements.append(Spacer(1, 6))
        
            
    if w_flags:
        # Warning Section
        elements.append(PageBreak())
        elements.append(Paragraph("List Part Warning!", bold_sub))
        elements.append(Spacer(1, 6))
        for idx, warning in enumerate(w_flags, start=1):
            elements.append(Paragraph(f"{idx}. {warning}", styles["Heading3"]))
            elements.append(Spacer(1, 3))
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            w_imgs[warning].save(tmp.name)
            orig_w, orig_h = w_imgs[warning].size
            if orig_h == 0:
                scale = 1.0
            else:
                scale = (MAX_IMG_HEIGHT) / orig_h
            pdf_w = orig_w * scale
            pdf_h = orig_h * scale
            img_flow = RLImage(tmp.name, width=pdf_w, height=pdf_h)
            img_flow.hAlign = "CENTER"
            elements.append(img_flow)
            elements.append(Spacer(1, 3))
            elements.append(Paragraph(f"Status / Ketebalan (mm) : {targets_and_data[warning]}", styles["Normal"]))
            elements.append(Spacer(1, 3))
            elements.append(Paragraph(f"Catatan :", styles["Normal"]))
            elements.append(Spacer(1, 2))
            elements.append(Paragraph(f"{w_notes[warning]}", styles["Normal"]))
            elements.append(Spacer(1, 6))
            
            if idx % 2 == 0 and idx<len(w_flags):
                elements.append(PageBreak())
    
    if b_flags:
        # Bad Section
        elements.append(PageBreak())
        elements.append(Paragraph("List Part Bad / Tidak Teridentifikasi / Tidak Ada!", bold_sub))
        elements.append(Spacer(1, 6))
        for idx, bad in enumerate(b_flags, start=1):
            elements.append(Paragraph(f"{idx}. {bad}", styles["Heading3"]))
            elements.append(Spacer(1, 3))
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            b_imgs[bad].save(tmp.name)
            orig_w, orig_h = b_imgs[bad].size
            if orig_h == 0:
                scale = 1.0
            else:
                scale = (MAX_IMG_HEIGHT) / orig_h
            pdf_w = orig_w * scale
            pdf_h = orig_h * scale
            img_flow = RLImage(tmp.name, width=pdf_w, height=pdf_h)
            img_flow.hAlign = "CENTER"
            elements.append(img_flow)
            elements.append(Spacer(1, 3))
            elements.append(Paragraph(f"Status / Ketebalan (mm) : {targets_and_data[bad]}", styles["Normal"]))
            elements.append(Spacer(1, 3))
            elements.append(Paragraph(f"Catatan :", styles["Normal"]))
            elements.append(Spacer(1, 2))
            elements.append(Paragraph(f"{b_notes[bad]}", styles["Normal"]))
            elements.append(Spacer(1, 6))
            
            if idx % 2 == 0 and idx<len(b_flags):
                elements.append(PageBreak())
            
    doc.build(elements)
    buffer.seek(0)
    return buffer

def create_report_inspections(part_name, identities, data, images):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    elements = []
    
    title_style = styles["Title"]
    elements.append(Paragraph(f"Laporan Inspeksi {part_name}", title_style))
    elements.append(Spacer(1, 12))
    
    identity = identities[:-1]
    identity.insert(4, "")
    comment = identities[-1]
    table_data = [identity[i:i+4] for i in range(0, 8, 4)]
    
    table_style = TableStyle([
        ("SPAN", (0, 0), (0, 1)),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ])
    
    identity_table = Table(table_data, colWidths=[doc.width / 4] * 4)
    identity_table.setStyle(table_style)
    elements.append(identity_table)
    elements.append(Spacer(1, 12))
    MAX_IMG_HEIGHT = 7.5 * cm
    
    bold_sub = ParagraphStyle(
        name="BoldSub",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        spaceAfter=6
    )
    
    # Komentar
    elements.append(Paragraph("Komentar dari Petugas:", bold_sub))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(f"{comment}", styles["Normal"]))
    elements.append(Spacer(1, 6))
    
    # All Data
    elements.append(Paragraph(f"Rincian Semua Part {part_name}!", bold_sub))
    elements.append(Spacer(1, 6))
    for idx, (target, part) in enumerate(data.items(), start=1): # data : target | image target_snake
        target_snake = target.lower().replace(" ", "_").replace("&", "and").replace("/", "_")
        elements.append(Paragraph(f"{idx}. {target}", styles["Heading3"]))
        elements.append(Spacer(1, 3))
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        images[f"{part_name}_{target_snake}_gambar"].save(tmp.name)
        orig_w, orig_h = images[f"{part_name}_{target_snake}_gambar"].size
        if orig_h == 0:
            scale = 1.0
        else:
            scale = (MAX_IMG_HEIGHT) / orig_h
        pdf_w = orig_w * scale
        pdf_h = orig_h * scale
        img_flow = RLImage(tmp.name, width=pdf_w, height=pdf_h)
        img_flow.hAlign = "CENTER"
        elements.append(img_flow)
        elements.append(Spacer(1, 3))
        elements.append(Paragraph(f"Jenis Pemeriksaan : {", ".join(str(i) for i in part["pemeriksaan"])}", styles["Normal"]))
        elements.append(Spacer(1, 3))
        elements.append(Paragraph(f"Status Kondisi : {part["condition"]}", styles["Normal"]))
        elements.append(Spacer(1, 3))
        elements.append(Paragraph(f"Kategori : {part["category"]}", styles["Normal"]))
        elements.append(Spacer(1, 3))
        elements.append(Paragraph(f"Remark : {part["remark"]}", styles["Normal"]))
        elements.append(Spacer(1, 6))
        
        if idx % 2 == 1 and idx<len(data.items()):
            elements.append(PageBreak())
            
    doc.build(elements)
    buffer.seek(0)
    return buffer