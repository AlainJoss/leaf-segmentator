import os
import streamlit as st
import shutil

##### FUNCTIONS #####

def save_data():
    OUTPUT_DIR = 'images/selected'
    with st.spinner("Saving ..."):
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        if 'further_process' in st.session_state:
            del st.session_state['further_process']
        else:
            st.session_state['further_process'] = []

        for i in range(len(img_paths)):  
            if st.session_state[f'select_{str(i)}'] != 'further process':
                selected_img_path = img_paths[i][int(st.session_state[f'select_{str(i)}'])]
                shutil.copy(selected_img_path, OUTPUT_DIR + '/')
            else:
                st.session_state['further_process'].append(i)
        
        rename_images(OUTPUT_DIR)

        st.session_state['further_processing'] = True

def rename_images(dir):
    file_names = os.listdir(dir)
    for old_name in file_names:
        # Keep only the first 12 characters of the filename
        new_name = old_name[0:12]
        # Only rename the file if the name has changed
        if new_name != old_name:
            os.rename(os.path.join(dir, old_name), os.path.join(dir, new_name))


##### PAGE #####

st.set_page_config(
    layout="wide",
    page_icon=":leaves:"
)

st.write('## Choose Final Images')

def image_paths(dir):
    return sorted([f'{dir}/{img}' for img in os.listdir(dir)])


if 'post_process' in st.session_state:
    if 'further_processing' not in st.session_state:

        st.write("""
        Steps:
        - For each row select the best segmented version of the image.
        - If no version satisfies your requirements select 'further process'
        - Save the selection by clicking on the button under the last image.
        """)

        DIR_SEGMENTED = 'images/segmented'
        DIR_IMAGES = 'images/cropped'
        img_paths_processed = image_paths(DIR_SEGMENTED)
        img_paths_images = image_paths(DIR_IMAGES)
        img_paths = []
        k = st.session_state['num_clusters'] - 1

        # Create column groups
        for i in range(0, len(img_paths_processed), k):
            group = img_paths_processed[i:i+k]
            if img_paths_images:  # There are still images in the 'images' directory
                group.insert(0, img_paths_images.pop(0)) 
            img_paths.append(group)

        select_options = [str(i) for i in range(1, k+1)] + ['further process']

        # Selection grid
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

            # Enable next step
            if st.form_submit_button(label='Save Selection', on_click=save_data):
                st.session_state['further_processing'] = True
                st.experimental_rerun()
    else:
        st.session_state['further_processing'] = True
        st.success("You can now further process the images!")
else: 
    st.error("Go back to 'segment' to enable this step.")