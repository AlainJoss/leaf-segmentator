import streamlit as st
import os
from PIL import Image


##### FUNCTIONS #####

def process_image(img_path, slider_value):
    img = Image.open(img_path)
    # Draw a white color on everything above the slider_value (scaled to the original image size)
    for i in range(img.width):
        for j in range(int(slider_value)):
            img.putpixel((i,j), (255,255,255))  # Set the color to white
    return img

def save_image(img):
    st.session_state['processed_images'].append(img)

def save_images():
    DIR = 'stem_cutted_leafs'
    os.makedirs(DIR, exist_ok=True)

    for i, img in enumerate(st.session_state["processed_images"]):
        filename = f'{DIR}/{st.session_state["img_paths"][i]}'
        img.save(filename)


##### SESSION STATES #####

if 'idx' not in st.session_state:
    st.session_state['idx'] = 0

if 'img_paths' not in st.session_state:
    img_paths = os.listdir('images')
    img_paths.sort()
    img_paths.pop(0)
    st.session_state['img_paths'] = img_paths
    st.session_state['folder_size'] = len(img_paths)

if 'processed_images' not in st.session_state:
    st.session_state['processed_images'] = list()

if 'finished_processing' not in st.session_state:
    st.session_state['finished_processing'] = False


##### FRONTEND #####

st.title("Cut Stems")

st.write("Cut the upper part of the leaf, moving the slider where the stem begins.")


##### PROCESSING #####

if not st.session_state['finished_processing']:
    idx = st.session_state['idx']

    if idx < st.session_state['folder_size']: 
        img_path = st.session_state['img_paths'][idx]
        img_path = 'images/' + img_path 
        img = Image.open(img_path)
        img.thumbnail((600, 600))  # Resize to fit within 600x600 box, maintaining aspect ratio

        slider_value = st.slider("Slide to cut the stem", 0, img.height, value=0)
        
        processed_image = process_image(img_path, slider_value)
        st.image(processed_image, caption="Processed Image")  # Display the processed image

        if st.button("Save --> go to next image"):
            save_image(processed_image)
            st.session_state['idx'] = idx + 1  # move to next image
            
            if st.session_state['idx'] == st.session_state['folder_size']:
                save_images()
                st.session_state['finished_processing'] = True

            st.experimental_rerun()
else:
    st.success('You successfully cut all stems!')
