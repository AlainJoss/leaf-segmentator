import streamlit as st
import os
from PIL import Image
import numpy as np

st.write("## Rotate and Cut Stems")

if 'cut_stems' in st.session_state:

    if 'crop_images' not in st.session_state:

        st.write("Rotate and cut the upper part of the leaf, moving the sliders as needed.")

        ##### FUNCTIONS #####

        def rotate_image(img_path, rotation_value):
            img = Image.open(img_path)
            rotated_img = img.rotate(rotation_value, expand=True)  # Rotate the image
            return rotated_img

        def process_image(img, slider_value):
            img_array = np.array(img)  # Convert image to NumPy array
            img_array[:slider_value, :] = 255  # Set all pixel values above the slider_value to white (255)

            processed_img = Image.fromarray(img_array)  # Convert NumPy array back to PIL image
            return processed_img


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
            st.session_state['img_paths'] = img_paths
            st.session_state['folder_size'] = len(img_paths)

        if 'processed_images' not in st.session_state:
            st.session_state['processed_images'] = list()

        if 'finished_processing' not in st.session_state:
            st.session_state['finished_processing'] = False


        ##### PROCESSING #####

        if not st.session_state['finished_processing']:
            idx = st.session_state['idx']

            if idx < st.session_state['folder_size']: 
                img_path = st.session_state['img_paths'][idx]
                img_path = 'images/' + img_path 
                img = Image.open(img_path)

                # Create a copy of the image for display purposes
                display_img = img.copy()
                display_img.thumbnail((600, 600))  # Resize the display image to fit within 600x600 box, maintaining aspect ratio

                rotation_value = st.slider("Slide to rotate the image", -180, 180, value=0, step=90)
                rotated_image = rotate_image(img_path, rotation_value)
                            
                slider_value = st.slider("Slide to cut the stem", 0, rotated_image.height//10, value=0)
                            
                processed_image = process_image(rotated_image, slider_value)

                # Create a copy of the processed image for display purposes
                display_processed_image = processed_image.copy()
                display_processed_image.thumbnail((600, 600))  # Resize the processed image for display

                st.image(display_processed_image, width=500)  # TODO: OR USE COLUMN WIDTH

                col1, col2, col3 = st.columns([1.5,3.8,1])  # Adjust the second column weightage to suit your needs

                with col1:
                    if st.button("Previous Image"):
                        st.session_state['idx'] = idx - 1  # move to next image

                        st.experimental_rerun()

                with col3:  # changed from col2 to col3
                    if st.button("Next Image"):
                        save_image(processed_image)

                        if st.session_state['idx'] == st.session_state['folder_size'] - 1:
                            save_images()
                            st.session_state['finished_processing'] = True
                        else:
                            st.session_state['idx'] = idx + 1  # move to next image

                        st.experimental_rerun()

            
        else:
            st.session_state['crop_images'] = True
            st.experimental_rerun()
    else:
        st.success("You can now segment the images!") 

else: 
    st.error("Go back to upload images to enable this step.")
