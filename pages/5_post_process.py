import os
import pandas as pd
import streamlit as st

def save_data():
    st.session_state['mask_selected'] = True
    data = {'Group': [], 'Selection': []}
    for i in range(len(img_paths)):  # Use img_paths instead of groups
        data['Group'].append(i)
        data['Selection'].append(st.session_state[f'select_{str(i)}'])
    df = pd.DataFrame(data)
    df.to_csv('selections.csv', index=False)
    st.success('Selections saved!')

st.set_page_config(
    layout="wide"
)

st.write('## Choose Final Images')

def image_paths(dir):
    return sorted([f'{dir}/{img}' for img in os.listdir(dir)])


if 'choose_image' in st.session_state:

    if 'define_conversion_rate' not in st.session_state:

        DIR_PROCESSED = 'processed_images'
        DIR_IMAGES = 'cropped_images'
        img_paths_processed = image_paths(DIR_PROCESSED)
        img_paths_images = image_paths(DIR_IMAGES)

        img_paths = []
        k = st.session_state['num_clusters'] - 1

        for i in range(0, len(img_paths_processed), k):
            group = img_paths_processed[i:i+k]
            if img_paths_images:  # There are still images in the 'images' directory
                group.insert(0, img_paths_images.pop(0)) 
            img_paths.append(group)

        select_options = [str(i) for i in range(1, k+1)] + ['further processing']

        if "mask_selected" not in st.session_state:
            with st.form(key='my_form'):
                for group in img_paths:
                    cols = st.columns(len(group) + 1) 
                    for i, img_path in enumerate(group):
                        # header
                        if i == 0:
                            cols[i].markdown("**original**")
                        elif i <= k:
                            cols[i].markdown(f"**{i}**")
                        cols[i].image(img_path)
                    key = f'select_{str(img_paths.index(group))}'
                    if key in st.session_state:
                        selection = cols[-1].selectbox("Select option:", select_options, key=key)
                    else:
                        selection = cols[-1].selectbox("Select option:", select_options, key=key)
                st.form_submit_button(label='Submit', on_click=save_data)

        if "mask_selected" in st.session_state:
            st.session_state['define_conversion_rate'] = True
            st.experimental_rerun()

    else:
        st.success("You can now define the conversion rate of the images!")

else: 
    st.error("Go back to 'post process' to enable this step.")