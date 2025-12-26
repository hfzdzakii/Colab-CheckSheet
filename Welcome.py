import streamlit as st
import base64
from pathlib import Path
from functions.helper import page_config

page_config()

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

BASE_DIR = Path(__file__).resolve().parents[0]
IMAGE_DIR = BASE_DIR / "images"

bg_base64_1 = get_base64_image(f"{IMAGE_DIR}/Gambar_Website_Col.jpg")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64_1}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        -webkit-backdrop-filter: blur(6px);
        backdrop-filter: blur(6px);
    }}
    
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }}
    
    @media (prefers-color-scheme: light) {{
        .stApp::before {{
            background: rgba(255, 255, 255, 0.85);
        }}
    }}

    @media (prefers-color-scheme: dark) {{
        .stApp::before {{
            background: rgba(0, 0, 0, 0.75);
        }}
    }}
    
    .main > div {{
        display: flex;
        justify-content: center;
    }}
    
    .card {{
        background-color: rgba(15,17,22,0.92);
        padding: 1.5rem;
        border-radius: 14px;
        max-width: 480px;
        margin: auto;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("AMOEBA")
st.subheader("Attachment Monitoring Base Application")

st.markdown("""
Platform digital untuk **monitoring kondisi attachment alat berat**
secara **digital, rapi, dan terdokumentasi**.
""")

st.markdown("""
### Kenapa AMOEBA?

AMOEBA membantu tim maintenance dan produksi
mendeteksi potensi kerusakan lebih dini melalui
pencatatan inspeksi yang akurat dan terstruktur.
""")

st.markdown("""
### Fitur Utama
            
✔ Pencatatan inspeksi lapangan berbasis web  
✔ Monitoring kondisi boom, arm, dan bucket  
✔ Pengecekan ketebalan & attachment  
✔ Riwayat inspeksi bisa diunduh
""")

st.markdown("### Mulai Sekarang!")

st.caption("Klik icon » di pojok kanan atas untuk membuka menu, atau klik link di bawah ini!")
st.page_link("pages/Check Sheet Inspeksi ARM.py", label="🦾 Inspeksi ARM")
st.page_link("pages/Check Sheet Inspeksi Boom.py", label="🏗️ Inspeksi Boom")
st.page_link("pages/Check Sheet Inspeksi Bucket.py", label="🪣 Inspeksi Bucket")
st.page_link("pages/Check Sheet Ketebalan Bucket.py", label="📏 Ketebalan Bucket")