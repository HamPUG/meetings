# https://gradio.app/interface-state/#global-state

import gradio as gr

scores = []

def track_score(score):
    scores.append(score)
    top_scores = sorted(scores, reverse=True)[:3]
    return top_scores

demo = gr.Interface(
    fn=track_score, 
    inputs=gr.Number(label="Score"), 
    outputs=gr.JSON(label="Top Scores")
)
demo.launch()

