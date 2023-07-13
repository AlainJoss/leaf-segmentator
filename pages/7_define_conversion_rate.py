import streamlit as st
from PIL import Image, ImageDraw
import math
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(
    layout="wide"
)

st.write("""
## Define the Conversion Rate
""")
        
if 'define_conversion_rate' in st.session_state:
    if 'finalize' not in st.session_state:

        st.write("""
            The conversion rate $r$ is defined as: $r = cm^2/pixel$.

            Steps:
            - Read in your conversion image image with the ruler.
            - Place the blue line over the ruler.
            - Write the real world distance in the text area below.
            - Compute the conversion rate.
        """)

        # Pick conversion image
        image_file = st.file_uploader("Select your conversion image.")
        st.write("#### Overlay the blue line on the ruler by adjusting the sliders.")
        if image_file is not None:
            image_original = Image.open(image_file)
            image_conversion = image_original.copy() 
            image_width, image_height = image_conversion.size

            x_default_1 = int(image_width * 0.25)
            x_default_2 = int(image_width * 0.75)
            y_default_1 = int(image_height * 0.45)
            y_default_2 = int(image_height * 0.55)
            x1_tape, x2_tape = st.slider('x1, x2', min_value=0, max_value=image_width, value=[x_default_1, x_default_2], step=1)
            y1_tape, y2_tape = st.slider('y1, y2', min_value=0, max_value=image_height, value=[y_default_1, y_default_2], step=1)

            draw = ImageDraw.Draw(image_conversion)

            pixel_distance = 0
            if x1_tape and y1_tape and x2_tape and y2_tape:
                draw.line(((x1_tape, y1_tape), (x2_tape, y2_tape)), fill="blue", width=5)
                st.image(image_conversion, use_column_width=True)

                pixel_distance = math.sqrt((x2_tape - x1_tape)**2 + (y2_tape - y1_tape)**2)
            
            st.write("#### Compute and save the conversion rate.")

            real_distance = st.number_input("Enter the real-world distance (in cm) on your ruler", min_value=0.0, step=0.1)

            if real_distance == 0:
                st.write(fr"**Conversion rate**: {0} $pixel/cm^2$")
                st.session_state['conversion_rate'] = 0
            else:
                conversion_rate = (real_distance / pixel_distance)**2
                st.session_state['conversion_rate'] = conversion_rate
                st.write(fr"**Conversion rate**: {round(conversion_rate, 5)} $pixel/cm^2$")

            # Enable next step
            if st.button('Save Conversion Rate'):
                st.session_state['finalize'] = True
                st.experimental_rerun()
    else:
        st.session_state['finalize'] = True
        st.success("You can now create the final report!")
else: 
    st.error("Go back to 'further process' to enable this step.")