import streamlit as st
import pandas as pd
from ocr import ocr_to_df


def main():
    st.title("OCR Data Extraction App")

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    uploaded_files = st.file_uploader("Upload image files",
                                      type=["png", "jpg", "jpeg"],
                                      accept_multiple_files=True,
                                      key=st.session_state["file_uploader_key"])

    if uploaded_files:
        st.session_state["uploaded_files"] = uploaded_files

    if not uploaded_files:
        st.warning("Please upload valid image files.")
        return

    st.write("Scanning images...")

    df_list = []
    progress_bar = st.progress(0)

    for i, uploaded_file in enumerate(uploaded_files):
        # Perform OCR and create DataFrame for each uploaded image
        df_list.append(ocr_to_df(uploaded_file))
        progress_bar.progress((i + 1) / len(uploaded_files))

    # Consolidate data from all uploaded images
    merged_df = pd.concat(df_list, ignore_index=True)
    merged_df = merged_df.drop_duplicates()
    merged_df.reset_index(drop=True, inplace=True)

    st.write("Full Data:")
    st.dataframe(merged_df)

    st.write("")
    st.write("Download Data:")
    st.button("Download merged Excel", on_click=download_merged_excel, args=(merged_df,))


def download_merged_excel(merged_df):
    excel_filename = "merged_data.xlsx"
    merged_df.to_excel(excel_filename, index=False)
    st.success(f"Download successful: [{excel_filename}](./{excel_filename})")
    st.session_state["file_uploader_key"] += 1
    st.rerun()


if __name__ == "__main__":
    main()
