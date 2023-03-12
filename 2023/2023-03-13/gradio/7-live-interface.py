# https://gradio.app/reactive-interfaces/#live-interfaces

import gradio as gr

def calculator(num1, operation, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        return num1 / num2

demo = gr.Interface(
    fn=calculator,
    inputs=[
        "number",
        gr.Radio(["add", "subtract", "multiply", "divide"]),
        "number"
    ],
    outputs="number",
    live=True,
)
demo.launch()

