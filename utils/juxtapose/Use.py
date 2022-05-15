import streamlit.components.v1 as components
import cv2 as cv
from PIL import Image
import pathlib
import streamlit as st

def superView(raw_image,segmented_img,IMG1,IMG2,height: int = 1000):
    cdn_path = "https://cdn.knightlab.com/libs/juxtapose/latest"
    css_block = f'<link rel="stylesheet" href="{cdn_path}/css/juxtapose.css">'
    js_block = f'<script src="{cdn_path}/js/juxtapose.min.js"></script>'


    STREAMLIT_STATIC_PATH = (
        pathlib.Path(st.__path__[0]) / "static"
    )
    Image1 = Image.fromarray(cv.cvtColor(raw_image, cv.COLOR_GRAY2RGB))
    Image2 = Image.fromarray(cv.cvtColor(segmented_img, cv.COLOR_BGR2RGB))
    Image1.save(STREAMLIT_STATIC_PATH / IMG1)
    Image2.save(STREAMLIT_STATIC_PATH / IMG2)



    # write html block
    htmlcode = (
        css_block
        + """ 
        """
        + js_block
        + """
            <div id="foo" style="width: 95%; height: """
        + str(height)
        + '''px; margin: 1px;"></div>
            <script>
            slider = new juxtapose.JXSlider('#foo',
                [
                    {
                        src: "'''
        + IMG1
        + '''",
                        label: 'Raw',
                    },
                    {
                        src: "'''
        + IMG2
        + """",
                        label: 'Segmentation',
                    }
                ],
                {
                    animate: true,
                    showLabels: true,
                    showCredits: true,
                    startingPosition: "50%",
                    makeResponsive: true
                });
            </script>
        """
    )
    static_component = components.html(
        htmlcode,
        height=height,
    )

    return static_component