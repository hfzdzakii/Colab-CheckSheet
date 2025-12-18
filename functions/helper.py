import streamlit as st
import time
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
        bad_notes=st.session_state.bad_notes
    )
    
@dataclass
class AppStateARMInspection:
    submitted: bool = False
    pdf_download:bool = False
    data: dict = field(default_factory=dict)

def init_state_arm_inspection(targets:list) -> AppStateARMInspection:
    st.session_state.setdefault("submitted", False)
    st.session_state.setdefault("pdf_download", False)
    st.session_state.setdefault("data", {})
    for target in targets:
        st.session_state.data.setdefault(
            target,
            {
                "pemeriksaan": None,
                "condition": None,
                "category": None,
                "remark": None,
                "image": None,
            }
        )
    return AppStateARMInspection(
        submitted=st.session_state.submitted,
        pdf_download=st.session_state.pdf_download,
        data=st.session_state.data,
    )

# @dataclass
# class AppStateBoomInspection:
#     form_submitted: bool = False # <- Form nononono
#     pdf_download:bool = False
#     open_camera_name: str | None = None
#     safe_images:dict = field(default_factory=dict)
#     warning_images:dict = field(default_factory=dict)
#     bad_images:dict = field(default_factory=dict)

# def init_state_boom_inspection() -> AppStateBoomInspection:
#     for key, default in AppStateARMInspection().__dict__.items():
#         st.session_state.setdefault(key, default)
#     return AppStateBoomInspection(
#         form_submitted=st.session_state.form_submitted,
#         pdf_download=st.session_state.pdf_download,
#         open_camera_name=st.session_state.open_camera_name,
#         safe_images=st.session_state.safe_images,
#         warning_images=st.session_state.warning_images,
#         bad_images=st.session_state.bad_images,
#     )

# @dataclass
# class AppStateBucketInspection:
#     form_submitted: bool = False
#     pdf_download:bool = False
#     open_camera_name: str | None = None
#     safe_images:dict = field(default_factory=dict)
#     warning_images:dict = field(default_factory=dict)
#     bad_images:dict = field(default_factory=dict)

# def init_state_bucket_inspection() -> AppStateBucketInspection:
#     for key, default in AppStateARMInspection().__dict__.items():
#         st.session_state.setdefault(key, default)
#     return AppStateBucketInspection(
#         form_submitted=st.session_state.form_submitted,
#         pdf_download=st.session_state.pdf_download,
#         open_camera_name=st.session_state.open_camera_name,
#         safe_images=st.session_state.safe_images,
#         warning_images=st.session_state.warning_images,
#         bad_images=st.session_state.bad_images,
#     )

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
    return st.number_input(message, max_value=help["std"], min_value=0.0, format="%.2f", placeholder="Gunakan titik (.) sebagai pengganti koma (,)", help=f"std:{help["std"]}, min:{help["min"]}", value=None)

def input_text(message):
    return st.text_input(message, value=None)

def create_inspection_inputs2(names_snake):
    col1, col2 = st.columns(2)
    with col1:
        input_multiselect("Jenis Pemeriksaan", "pemeriksaan", f"{names_snake}_pemeriksaan")
        input_selectbox("Jenis Kondisi", "condition", f"{names_snake}_condition")
    with col2:
        input_selectbox("Kategori", "category", f"{names_snake}_category")
        input_selectbox("Remark", "remark", f"{names_snake}_remark")
    checkbox_key = f"{names_snake}_checkbox"
    camera_key = f"{names_snake}_gambar"
    st.checkbox("Buka Kamera", key=checkbox_key)
    enable = st.session_state.get(checkbox_key, False)
    st.camera_input("Take a picture", disabled=not enable, key=camera_key)

def apply_data_inspection(names, names_snake):
    for name, name_snake in list(zip(names, names_snake)):
        st.session_state.data[name] = {
            "pemeriksaan": st.session_state[f"{name_snake}_pemeriksaan"],
            "condition": st.session_state[f"{name_snake}_condition"],
            "category": st.session_state[f"{name_snake}_category"],
            "remark": st.session_state[f"{name_snake}_remark"],
            "image": st.session_state[f"{names_snake}_gambar"],
        }

def create_inspection_inputs(name):
    col1, col2 = st.columns(2)
    with col1:
        pemeriksaan = input_multiselect("Jenis Pemeriksaan", "pemeriksaan", None)
        condition = input_selectbox("Jenis Kondisi", "condition", None)
    with col2:
        category = input_selectbox("Kategori", "category", None)
        remark = input_selectbox("Remark", "remark", None)
    img_slot = st.empty()
    saved_img = st.session_state.images.get(name)
    if saved_img is not None:
        img_slot.image(saved_img, caption=f"📷 Dokumentasi tersimpan: {name}", width=200)
        if st.button("Ambil ulang gambar!", icon=":material/camera:", disabled=False if st.session_state.open_camera_name==None else True):
            st.session_state.open_camera_name = name
            st.rerun()
    else :
        if st.button("Klik untuk membuka Kamera!", type="primary", icon=":material/camera:", disabled=False if st.session_state.open_camera_name==None else True):
            st.session_state.open_camera_name = name
            st.rerun()
    if st.session_state.open_camera_name == name:
        photo = st.camera_input(f"Upload Dokumentasi - {name}!")
        if photo is not None:
            if st.button("Klik untuk menyimpan foto!", icon=":material/upload:", type="primary"):
                try:
                    image = Image.open(photo)
                    st.session_state.images[name] = image
                    img_slot.image(image, caption=f"📷 Dokumentasi tersimpan: {name}", width=200)
                    photo = None
                    st.session_state.open_camera_name = None
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error : {e}")
    return pemeriksaan, condition, category, remark

@st.dialog("Yakin melakukan Reset?")
def reset_confirmation():
    st.write("Melakukan reset akan menghilangkan semua data.")
    with st.spinner("Tunggu..."):
        time.sleep(3)
    if st.button("Reset!", type="primary", icon=":material/delete:", width="stretch"):
        for key in st.session_state.keys():
            del st.session_state[key]
        
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
        return [nama_processed, code_unit_processed, egi_processed,
                district_processed, hours_meter_processed, date_processed,
                periode_service_processed]

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
    
    identity_table = Table(table_data, colWidths=[None, None, None])
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