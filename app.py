import os
import streamlit as st
import pandas as pd
from ocr import ocr_to_df


def main():
    st.title("OCR Data Extraction App")

    folder_path = st.text_input("Enter the path to the folder of images:", key="folder_path")

    if folder_path and os.path.exists(folder_path) and os.path.isdir(folder_path):
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not image_files:
            st.warning("No valid images found in the folder.")
            return

        st.write("Scanning images...")

        df_list = []
        progress_bar = st.progress(0)

        for i, image_file in enumerate(image_files):
            image_path = os.path.join(folder_path, image_file)

            # Perform OCR and create DataFrame for each image
            df_list.append(ocr_to_df(image_path))
            progress_bar.progress((i + 1) / len(image_files))

        # Consolidate data from all images
        merged_df = pd.concat(df_list, ignore_index=True)
        merged_df = merged_df.drop_duplicates()

        st.write("Full Data:")
        st.dataframe(merged_df)

        st.write("")
        st.write("Download Data:")
        st.button("Download merged Excel", on_click=download_merged_excel, args=(merged_df,))


def download_merged_excel(merged_df):
    excel_filename = "merged_data.xlsx"
    merged_df.to_excel(excel_filename, index=False)
    st.success(f"Download successful: [{excel_filename}](./{excel_filename})")


if __name__ == "__main__":
    main()
