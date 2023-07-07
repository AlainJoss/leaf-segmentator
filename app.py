import os
import pandas as pd
import streamlit as st

def save_data():
    st.session_state.submit_button = True
    data = {'Group': [], 'Selection': []}
    for i in range(len(groups)):
        data['Group'].append(i)
        data['Selection'].append(st.session_state[f'select_{str(i)}'])
    df = pd.DataFrame(data)
    df.to_csv('selections.csv', index=False)
    st.success('Selections saved!')

st.set_page_config(
    layout="wide"
)

st.title('Segmented Leafs')
st.write('For each row select the best processed image:')

def image_paths(dir):
    return os.listdir(dir)

DIR = 'processed_images'
img_paths = image_paths(DIR)
img_paths = sorted(img_paths)

if img_paths[0] == '.DS_Store':
    img_paths.remove('.DS_Store')

for idx, img_path in enumerate(img_paths):
    img_paths[idx] = f'{DIR}/{img_path}'

groups = []
k = 3  # Change k to 4 because you want 4 images per row
for i in range(0, len(img_paths), k):
    groups.append(img_paths[i:i+k])

if "submit_button" not in st.session_state or not st.session_state.submit_button:
    with st.form(key='my_form'):
        for group in groups:
            cols = st.columns(k+1)  # We add an extra column for the text input
            for i, img_path in enumerate(group):
                cols[i].image(img_path)
            key = f'select_{str(groups.index(group))}'
            if key in st.session_state:
                selection = cols[k].selectbox("Select option:", ['further processing', '1', '2', '3'], key=key, value=st.session_state[key])
            else:
                selection = cols[k].selectbox("Select option:", ['further processing', '1', '2', '3'], key=key)
        st.form_submit_button(label='Submit', on_click=save_data)

if "submit_button" in st.session_state and st.session_state.submit_button:
    st.write('Your selections have been saved. Refresh the page to make new selections.')
