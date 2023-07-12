import os
import pandas as pd
import streamlit as st
import shutil

# TODO: only for faster testing purposes



def save_data():
    with st.spinner("Saving ..."):
        if os.path.exists('selected_images'):
            shutil.rmtree('selected_images')
        os.makedirs('selected_images', exist_ok=True)
        if 'further_processing' in st.session_state:
            del st.session_state['further_processing']
        if 'further_processing' not in st.session_state:
            st.session_state['further_processing'] = []
        for i in range(len(img_paths)):  # Use img_paths instead of groups
            # If the image is selected, copy it to the new directory
            if st.session_state[f'select_{str(i)}'] != 'further processing':
                selected_img_path = img_paths[i][int(st.session_state[f'select_{str(i)}'])]
                shutil.copy(selected_img_path, 'selected_images/')
            else:
                st.session_state['further_processing'].append(i)

st.write('## Choose Final Images')

def image_paths(dir):
    return sorted([f'{dir}/{img}' for img in os.listdir(dir)])


if 'choose_image' in st.session_state:

    if 'further_processing' not in st.session_state:

        DIR_PROCESSED = 'processed_images'
        DIR_IMAGES = 'cropped_images'
        img_paths_processed = image_paths(DIR_PROCESSED)
        img_paths_images = image_paths(DIR_IMAGES)

        img_paths = []

        # TODO: REMOVE
        st.session_state['num_clusters'] = 4

        k = st.session_state['num_clusters'] - 1

        for i in range(0, len(img_paths_processed), k):
            group = img_paths_processed[i:i+k]
            if img_paths_images:  # There are still images in the 'images' directory
                group.insert(0, img_paths_images.pop(0)) 
            img_paths.append(group)

        select_options = [str(i) for i in range(1, k+1)] + ['further processing']


        with st.form(key='selection'):
            for group in img_paths:
                cols = st.columns(len(group) + 1)
                for i, img_path in enumerate(group):
                    # header
                    if i == 0:
                        cols[i].markdown("**original**")
                    elif i <= k:
                        cols[i].markdown(f"**{i}**")
                    # image
                    cols[i].image(img_path)
                key = f'select_{str(img_paths.index(group))}'
                selection = cols[-1].selectbox("Select option:", select_options, key=key)

            if st.form_submit_button(label='Save Selection', on_click=save_data):
                st.session_state['further_processing'] = True
                st.experimental_rerun()

    else:
        st.success("You can now define the conversion rate of the images!")

else: 
    st.error("Go back to 'segment' to enable this step.")