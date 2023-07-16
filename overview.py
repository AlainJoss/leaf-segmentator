import streamlit as st
import os
import shutil


##### FUNCTIONS #####

def remove_if_exists(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)



##### PAGE #####

st.set_page_config(
    layout="wide",
    page_icon=":leaves:"
)

st.title('Leaf Segmentator')

##### LOGIC #####

if 'upload' not in st.session_state:
    if st.button("Start Processing"):

        # Remove older states
        remove_if_exists(path='images')
        remove_if_exists(path='results.xlsx')

        # Enable next step
        st.session_state['upload'] = True

        st.experimental_rerun()

else:
    st.success("You can now upload your images!")

st.write(r"""
#### Purpose
This application enables you to segment leaf images and convert the segmented area from pixels to square centimeters.

#### A few details
- The app is optimized for images taken against a white background.
- To use images taken against different backgrounds, you'll need to modify the app's backend.

#### Here's how to use it
1. Upload your leaf images as a zip file.
2. Rotate the images such that the leafs are upside-down, and cut the stem.
3. Crop the unused contours of the image, which could interfer with the segmentation.
4. Segment the images, adjusting the given parameters.
5. Select the best segmented version for each image. If you're not satisfied with any version, choose to process it further.
6. If required, select images for further processing.
7. Define the conversion rate of cm² per pixel to calculate the leaf areas.
8. Download the report generated by the app.

#### Some tips for a smooth experience
- Follow the instructions on the user interface (UI).
- The instructions will guide you through each page, one step at a time.
- Please be patient and allow the app to fully execute each instruction to avoid crashing.
- If an error occurs at any point, refresh your browser and start over.
- Don't refresh your browser unless the app crashes, as you may lose your progress.

""")
