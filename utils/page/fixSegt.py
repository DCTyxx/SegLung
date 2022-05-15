import streamlit as st
import cv2 as cv
from PIL import Image
import numpy as np

# import streamlit_drawable_canvas
from ..sdcd import streamlit_drawable_canvas


def fixResult(raw_imagex,pre_imagex,file):
    with st.container():
        # st.header("Others")
        col1, col2 = st.columns([5, 5])
        raw_image = Image.fromarray(cv.cvtColor(raw_imagex, cv.COLOR_BGR2RGB))
        pre_image = Image.fromarray(cv.cvtColor(pre_imagex, cv.COLOR_BGR2RGB))
        img = streamlit_drawable_canvas._resize_img(raw_image,new_height= 600, new_width= 600)
        pre = streamlit_drawable_canvas._resize_img(pre_image, new_height=600, new_width=600)
        with col1:


            # Specify canvas parameters in application
            drawing_mode = st.sidebar.selectbox(
                "Drawing tool:", ("polygon","point", "rect", "circle", "transform")
            )
            if drawing_mode != 'polygon' :
                point_display_radius = st.sidebar.slider("Point display radius: ", 0, 25, 15)

            if drawing_mode=="polygon":
                stroke_width = st.sidebar.slider("Stroke width: ", 0, 5, 1)


            stroke_color = st.sidebar.color_picker("Stroke color hex: ","#ffffff")
            bg_color = st.sidebar.color_picker("Background color hex: ", "#000000")
            realtime_update = st.sidebar.checkbox("Update in realtime", False)

            # Create a canvas component
            canvas_result = streamlit_drawable_canvas.st_canvas(
                fill_color="rgba(67, 0, 100, 0.5)",  # Fixed fill color with some opacity
                stroke_width=stroke_width if drawing_mode == 'polygon'else 0,
                stroke_color=stroke_color,
                background_color=bg_color,
                background_image=img,
                update_streamlit=realtime_update,
                height=600,
                width = 600,
                drawing_mode=drawing_mode,
                point_display_radius=point_display_radius if drawing_mode != 'polygon' else 0,
                key="canvas",
            )

            if canvas_result.image_data is not None:
                img = cv.cvtColor(np.asarray(canvas_result.image_data), cv.COLOR_RGB2BGR)
                img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                ret, thresh1 = cv.threshold(img, 0, 255, cv.THRESH_BINARY)
                cv.imwrite(filename=file, img=thresh1)

        with col2:
            st.image(pre)

    # Do something interesting with the image data and paths
    # if canvas_result.image_data is not None:
    #     st.image(canvas_result.image_data)