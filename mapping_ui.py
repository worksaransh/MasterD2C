"""Minimal manual mapping UI contract using Streamlit dropdowns.

Run:
    streamlit run mapping_ui.py
"""

import streamlit as st

from d2c_ingestion.pipeline import process_upload
from d2c_ingestion.template_store import TemplateStore

st.title("Upload + Mapping Engine")

upload = st.file_uploader("Upload Shopify or Meta Ads file", type=["csv", "xlsx"])
template_key = st.selectbox("Template", ["shopify", "meta_ads"])

if upload:
    temp_path = f"/tmp/{upload.name}"
    with open(temp_path, "wb") as f:
        f.write(upload.getbuffer())

    result = process_upload(temp_path, template_key)
    st.subheader("Missing Required Fields")
    if result["errors"]:
        for err in result["errors"]:
            st.error(err)
    else:
        st.success("All required fields are mapped")

    st.subheader("Manual Mapping")
    final_mapping = {}
    for row in result["manual_mapping_ui"]:
        selected = st.selectbox(
            f"{row['system_field']} (suggested: {row['suggested_column']}, conf: {row['confidence']:.1f})",
            row["select_options"],
            index=(row["select_options"].index(row["suggested_column"]) if row["suggested_column"] in row["select_options"] else 0),
        )
        final_mapping[row["system_field"]] = None if selected == "-- Unmapped --" else selected

    template_name = st.text_input("Template name", value=f"{template_key}_mapping")

    if st.button("Save Mapping Template"):
        store = TemplateStore()
        template_id = store.save_mapping_template(
            name=template_name,
            source_type=template_key,
            columns=result["columns"],
            mapping={k: v for k, v in final_mapping.items() if v},
        )
        st.success(f"Template saved with id: {template_id}")

    st.subheader("Preview")
    st.dataframe(result["preview"])
