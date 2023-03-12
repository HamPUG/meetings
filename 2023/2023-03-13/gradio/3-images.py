# https://gradio.app/quickstart/#an-image-example

import numpy as np
import gradio as gr

def sepia(input_img):
    # images get supplied as numpy arrays
    sepia_filter = np.array([
        [0.393, 0.769, 0.189], 
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    # ...and returned as such as well
    return sepia_img

demo = gr.Interface(fn=sepia, inputs=gr.Image(shape=(200, 200)), outputs="image")
# if you want to define the size of the output image as well:
#demo = gr.Interface(fn=sepia, inputs=gr.Image(shape=(200, 200)), outputs=gr.Image().style(height=200, width=200))
demo.launch()

