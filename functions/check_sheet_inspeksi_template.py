import streamlit as st
from datetime import datetime
from collections import defaultdict
from functions.helper import page_config, input_text, input_radio, create_inspection_inputs, process_identities, create_report_inspections, apply_data_inspection, pdf_dialog, nav_and_back

# ==========
def inspection_template(part_name, data, targets, targets_snake):
    nav_and_back()
    
    st.title(f"Inspeksi {part_name}")
    st.caption("Klik » di pojok kiri atas untuk melihat gambar part!")

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
        create_inspection_inputs(part_name, target_snake)
    # ====
    st.subheader("Mechanic / Welder Comment")
    comment = st.text_area("📝 Masukkan Komentar Setelah Inspeksi!")

    submitted = st.button("Simpan", disabled=False if st.session_state[f"{part_name}_open_camera_name"]==None else True, type="primary")
        
    #  ===============================    
    identities = [nama, code_unit, egi, district, hours_meter, 
                    date, periode_service, comment]

    if submitted:
        apply_data_inspection(part_name, targets, targets_snake)
        
        if any((field == 0.0 or field == None or field == "") for field in identities):
            st.error("❌ Data Identitas atu catatan ada yang kosong. Silahkan diisi semuanya!")
            st.stop()
            
        for target, fields in st.session_state[f"{part_name}_data"].items():
            if any(v in (None, "", "-", [], "[]") for v in fields.values()):
                st.error(f"❌ Data part {part_name} yang kosong, silahkan diisi semuanya!")
                parts_missing = [[keyz, keyzz] for keyz, valz in st.session_state[f"{part_name}_data"].items() for keyzz, valzz in valz.items() if valzz in (None, "", "-", [], "[]") ]
                dict_result = defaultdict(list)
                for part, detail in parts_missing:
                    dict_result[part].append(detail)
                for i, j in dict_result.items():
                    st.markdown(f"#### {i}")
                    for k in j:
                        st.markdown(f"- {k.title()}")
                st.write(st.session_state)
                st.stop()
                
        if any(st.session_state[f"{part_name}_images"].get(f"{part_name}_{name_snake}_gambar") is None for name_snake in targets_snake):
            st.error("❌ Ada gambar yang belum diambil. Silahkan ambil dokumentasinya!")
            st.write(st.session_state)
            st.stop()
                
        st.session_state[f"{part_name}_pdf_download"] = True
        st.rerun()

    if st.session_state[f"{part_name}_pdf_download"]:
        identities_processed = process_identities(identities, "inspection")
        pdf_buffer = create_report_inspections(part_name, identities_processed, st.session_state[f"{part_name}_data"], st.session_state[f"{part_name}_images"])
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        pdf_dialog(part_name, pdf_buffer, f"Report_Inspeksi_{part_name}_{timestamp}.pdf")
        