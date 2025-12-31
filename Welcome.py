import streamlit as st
from pathlib import Path
from functions.helper import page_config, get_base64_image

BASE_DIR = Path(__file__).resolve().parents[0]
IMAGE_DIR = BASE_DIR / "images"

bg_base64 = get_base64_image(f"{IMAGE_DIR}/Gambar_Website_Col.jpeg")
logo_base64 = get_base64_image(f"{IMAGE_DIR}/Logo.png")

page_config('zzz')

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
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
            background: rgba(0, 0, 0, 0.80);
        }}
    }}
    
    .main > div {{
        display: flex;
        justify-content: center;
    }}
    
    .top-left-image {{
        position: relative;
        top: 0px;
        width: 160px;
        z-index: 1000;
        margin: -50px 0px;
    }}
    
    </style>
    
    <img src="data:image/png;base64, {logo_base64}"
    class="top-left-image" alt="Logo KPP Mining">
    """,
    unsafe_allow_html=True
)

# st.image(IMAGE_DIR / "Logo.png", width=200)

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

st.caption("Klik icon » di pojok kiri atas untuk membuka menu, atau klik link di bawah ini!")
st.page_link("pages/Check Sheet Inspeksi ARM.py", label="🦾 Inspeksi ARM")
st.page_link("pages/Check Sheet Inspeksi Boom.py", label="🏗️ Inspeksi Boom")
st.page_link("pages/Check Sheet Inspeksi Bucket.py", label="🪣 Inspeksi Bucket")
st.page_link("pages/Check Sheet Ketebalan Bucket.py", label="📏 Ketebalan Bucket")