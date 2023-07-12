import streamlit as st
import os
import zipfile
import io
import shutil

st.write("## Upload Your Images")

if 'upload_images' in st.session_state:

    ##### UPLOAD #####
    if 'cut_stems' not in st.session_state:

        uploaded_file = st.file_uploader("Upload a zip of your images", type="zip")

        if uploaded_file is not None:
            byte_stream = io.BytesIO(uploaded_file.getbuffer())
            output_folder = 'images'

            with zipfile.ZipFile(byte_stream, 'r') as zip_ref:
                zip_ref.extractall(output_folder)

            macos_folder = os.path.join(output_folder, '__MACOSX')

            if os.path.exists(macos_folder):
                shutil.rmtree(macos_folder)

            st.success("Images successfully extracted!")

            ##### NEXT STEP #####

            st.session_state['cut_stems'] = True
            st.experimental_rerun()

    ##### IMAGE GRID #####
    else:
        st.success("You can now cut the stems of your leaves!")

        st.write("### Your images:")

        img_folder = 'images'
        st.session_state['original_image_paths'] = sorted(os.listdir(img_folder))

        img_paths = [os.path.join(img_folder, img) for img in os.listdir(img_folder)]
        K = 5
        groups = [img_paths[n:n+K] for n in range(0, len(img_paths), K)]

        for group in groups:
            cols = st.columns(len(group))
            for col, img_path in zip(cols, group):
                col.image(img_path, use_column_width=True)

else: 
    st.error("Go back to overview to enable this step.")
