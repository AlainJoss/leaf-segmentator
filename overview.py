import streamlit as st
import os
import shutil

st.set_page_config(
    layout="wide"
)

st.title('Leaf Segmentator')

st.write("""

#### TODO: 
- better name images or drop the last part of the name for report
- change post processing to be more manipolable
- clean and comment code base
- extract names of session states to file
- clean the repo-structure
- create data folders for images
- clean example notebook
- improve explanations on UI
- correct messages on UI
- Make explanation on overview.py about whole process
- Record screen cast with example
- Make read me with instructions about UI

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
