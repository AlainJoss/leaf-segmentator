import streamlit as st
import os
import shutil

st.set_page_config(
    layout="wide"
)

st.title('Leaf Segmentator')

st.write("""

Follow the steps:

- Visit one page after the other.
- Give the app the time to execute your instructions.
- Don't refresh the browser during the execution of instructions.

""")

if 'overview_button' not in st.session_state:
    if st.button("Start Processing"):
        if os.path.exists('images'):
            shutil.rmtree('images')
        if os.path.exists('stem_cutted_leafs'):
            shutil.rmtree('stem_cutted_leafs')
        if os.path.exists('cropped_images'):
            shutil.rmtree('cropped_images')   
            
        if 'upload_images' not in st.session_state:
            st.session_state['upload_images'] = True

        st.session_state['overview_button'] = True 

        st.experimental_rerun()

# Check the session variable before showing success message
else:
    st.success("You can now upload your images!")
