import gradio as gr
from generate import gradio_interface

# Gradio app
interface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Textbox(label="General Theme", placeholder="Enter a theme for the train, e.g., 'Mystery', 'Space', 'Fantasy'"),
        gr.Number(label="Number of Wagons (N)", value=5, precision=0),
        gr.Number(label="Minimum Passengers per Wagon", value=2, precision=0),
        gr.Number(label="Maximum Passengers per Wagon", value=5, precision=0)
    ],
    outputs=[
        gr.Textbox(label="LLM Json")
    ],
    title="Wagon Passcode and Passenger Generator",
    description="Generate unique wagon passcodes and dynamic passengers based on the train's theme and specifications!"
)

interface.launch()
