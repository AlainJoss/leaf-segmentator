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
    layout="wide"
)

st.title('Leaf Segmentator')

st.write(r"""

This app enables you to segment leaf images and translate the segmented area from $pixel$ to $cm^2$.

#### Some specifics
- The app was developed to segment images taken on a white background.
- If you want to be able to process other kinds of images you must change the backend of the app.

#### How it works
- Upload your images as a zip file.
- Rotate the images such that the leafs are positioned upside-down, and cut the stem.
- Crop the unused contours of the image, which could interfer with the segmentation.
- Segment the images by adjusting the given parameters.
- For each image select the best segmented version, or if no version satisfies your requirements, select further prossing.
- Further process the images you selected for this task.
- Define the conversion rate $cm^2/pixel$ to compute the leaf areas.
- Download the generated report.


#### Follow the steps

- Follow the instructions on the UI.
- The instructions will make you visit one page after the other and perform some task.
- Give the app the time to execute your instructions, otherwise it could crash.
- If at any point you encounter an error, refresh the browser and start fresh.
- Don't refresh the browser if the app doesn't crash, otherwise your progress will be lost.

""")
         

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
