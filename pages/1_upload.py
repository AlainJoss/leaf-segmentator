import streamlit as st
import os
import zipfile
import io
import shutil


##### FUNCTIONS #####

def upload_and_extract_zip(uploaded_file, output_folder):
    byte_stream = io.BytesIO(uploaded_file.getbuffer())

    with zipfile.ZipFile(byte_stream, 'r') as zip_ref:
        zip_ref.extractall(output_folder)

    # Removes os generated subfolder
    macos_folder = os.path.join(output_folder, '__MACOSX')

    if os.path.exists(macos_folder):
        shutil.rmtree(macos_folder)

def image_grid(img_paths, k=5):
    # Create column groups
    groups = [img_paths[n:n+k] for n in range(0, len(img_paths), k)]

    # Display the images
    for group in groups:
        cols = st.columns(k)
        for col, img_path in zip(cols, group):
            col.image(img_path, use_column_width=True)


##### PAGE #####

st.set_page_config(
    layout="wide",
    page_icon=":leaves:"
)

st.write("## Upload Your Images")

if 'upload' in st.session_state:

    OUTPUT_DIR = 'images/original'
    
    if 'cut_stems' not in st.session_state:

        st.write(r"""
        Steps:
        - Upload a zip file with all your images.
        - Make sure that your folder contains only images.
        """)

        uploaded_file = st.file_uploader("Upload a zip of your images", type="zip")

        if uploaded_file is not None:
            # Load images
            upload_and_extract_zip(uploaded_file, OUTPUT_DIR)
            
            # Enable next step
            st.success("Images successfully extracted!")
            st.session_state['cut_stems'] = True
            st.experimental_rerun()

    else:
        st.success("You can now rotate and cut the stems of your leaves!")
        st.write("#### Your images:")

        image_names = sorted(os.listdir(OUTPUT_DIR))

        st.session_state['image_names'] = image_names

        img_paths = [os.path.join(OUTPUT_DIR, img) for img in image_names]
        image_grid(img_paths, 5)

else: 
    st.error("Go back to 'overview' to enable this step.")
