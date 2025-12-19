import streamlit as st
from datetime import datetime
from functions.helper import page_config, input_text, input_radio, create_inspection_inputs2, process_identities, create_report_inspections, apply_data_inspection, pdf_dialog
page_config()

# ==========
def inspection_template(part_name, data, targets, targets_snake):
    st.title(f"Inspeksi {part_name}")

    st.header("Identitas")
    id1, id2 = st.columns(2)
    with id1:
        nama = input_text("Nama")
        code_unit = input_text("Code Unit")
        egi = input_text("EGI")
        district = input_text("District")
    with id2:
        hours_meter = input_text("Hours Meter")
        date = st.date_input("Tanggal Insp", value="today", disabled=True, format="DD/MM/YYYY", help="Otomatis terisi hari ini!")
        periode_service = input_radio("Periode Service", "periode")
        
    st.space("small")

    st.header(f"NDT {part_name}")
    # ====
    for idx, (target, target_snake) in enumerate(list(zip(targets, targets_snake)), start=1):
        st.subheader(f"{idx}\\. {target}", help="\n".join(str(i) for i in data[target_snake].values()))
        create_inspection_inputs2(target_snake)
    # ====
    st.subheader("Mechanic / Welder Comment")
    comment = st.text_area("📝 Masukkan Komentar Setelah Inspeksi!")

    submitted = st.button("Simpan", disabled=False if st.session_state.open_camera_name==None else True, type="primary")
        
    #  ===============================    
    identities = [nama, code_unit, egi, district, hours_meter, 
                    date, periode_service, comment]

    if submitted:
        apply_data_inspection(target, target_snake)
        
        if any((field == 0.0 or field == None or field == "") for field in identities):
            st.error("❌ Data Identitas atu catatan ada yang kosong. Silahkan diisi semuanya!")
            st.stop()
            
        for target, fields in st.session_state.data.items():
            if any(v in (None, "", "-") or (isinstance(v, list) and not v) for v in fields.values()):
                st.error(f"❌ Ada data part {part_name} yang kosong. Silahkan diisi semuanya!")
                st.stop()
                
        if any(st.session_state.images.get(f"{name_snake}_gambar") is None for name_snake in target_snake):
            st.error("❌ Ada gambar yang belum diambil. Silahkan ambil dokumentasinya!")
            st.stop()
                
        identities_processed = process_identities(identities, "inspection")
        st.session_state.pdf_download = True
        st.rerun()

    if st.session_state.pdf_download:
        pdf_buffer = create_report_inspections(part_name, identities, st.session_state.data, st.session_state.images)
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        pdf_dialog(pdf_buffer, f"Report_Inspeksi_{part_name}_{timestamp}.pdf")