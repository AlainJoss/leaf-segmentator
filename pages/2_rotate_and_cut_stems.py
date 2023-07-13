import streamlit as st
import os
from PIL import Image
import numpy as np


##### FUNCTIONS #####

def rotate_image(img_path, rotation_value):
    img = Image.open(img_path)
    rotated_img = img.rotate(rotation_value, expand=True)
    return rotated_img

def process_image(img, slider_value):
    img_array = np.array(img)  
    img_array[:slider_value, :] = 255 

    processed_img = Image.fromarray(img_array)  
    return processed_img


def save_image(img):
    st.session_state['processed'].append(img)

def save_images():
    DIR = 'images/stem_cutted'
    os.makedirs(DIR, exist_ok=True)

    for i, img in enumerate(st.session_state["processed"]):
        filename = f'{DIR}/{st.session_state["img_paths"][i]}'
        img.save(filename)


##### SESSION STATES #####

if 'idx' not in st.session_state:
    st.session_state['idx'] = 0

if 'img_paths' not in st.session_state:
    img_paths = os.listdir('images/original')
    img_paths.sort()
    st.session_state['img_paths'] = img_paths
    st.session_state['folder_size'] = len(img_paths)

if 'processed' not in st.session_state:
    st.session_state['processed'] = list()

if 'finished_processing' not in st.session_state:
    st.session_state['finished_processing'] = False


##### PAGE #####

st.set_page_config(
    layout="wide"
)

st.write("## Rotate and Cut Stems")

if 'cut_stems' in st.session_state:
    if 'crop' not in st.session_state:

        st.write(""" 
        Steps:
        - Rotate the images such that the leafs are placed upside-down.
        - Cut the stems, while keeping the leaf area intact.
        - The images are to be processed one-by-one.
        """)

        if not st.session_state['finished_processing']:
            idx = st.session_state['idx']

            if idx < st.session_state['folder_size']: 
                # Read correct image
                img_path = st.session_state['img_paths'][idx]
                img_path = 'images/original/' + img_path 
                img = Image.open(img_path)
                display_img = img.copy()

                # Display image 
                SIZE = 1000
                display_img.thumbnail((SIZE, SIZE)) 
                rotation_value = st.slider("Slide to rotate the image", -180, 180, value=0, step=90)
                rotated_image = rotate_image(img_path, rotation_value)     
                slider_value = st.slider("Slide to cut the stem", 0, rotated_image.height//10, value=0)   
                processed_image = process_image(rotated_image, slider_value)
                display_processed_image = processed_image.copy()
                display_processed_image.thumbnail((SIZE, SIZE))  

                # Go to next image
                if st.button("Next Image"):
                    save_image(processed_image)
                    if st.session_state['idx'] == st.session_state['folder_size'] - 1:
                        st.spinner("Saving ...")
                        save_images()
                        st.session_state['finished_processing'] = True
                    else:
                        st.session_state['idx'] = idx + 1  
                    st.experimental_rerun()

            st.image(display_processed_image, use_column_width=True) 
            
        # Enable next step
        else:
            st.session_state['crop'] = True
            st.experimental_rerun()
    else:
        st.session_state['crop'] = True
        st.success("You can now crop the images!") 
else: 
    st.error("Go back to 'upload' to enable this step.")
