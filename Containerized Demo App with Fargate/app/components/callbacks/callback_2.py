from app import app
from dash.dependencies import Input, Output, State
from transformers import pipeline

model = pipeline("text-classification", 
                 model="nlptown/bert-base-multilingual-uncased-sentiment")

@app.callback(
    [Output('output', 'children'), 
    Output('output', 'color'),
    Output('output', 'style')],
    [Input('submit-button', 'n_clicks'),
    State('input', 'value')]
    )
    
def analyse_sentiment(click, text):
    
    if (text is not None) | (len(text) > 0):
        visible = 'visible'
        output = model(text)[0]['label']
        
        if (output == "1 star") | (output == "2 stars"):
            text_output = f"☹️ {output} review"
            color = 'danger'
            
        elif output == "3 stars":
            text_output = f"😐 {output} review"
            color = 'secondary'
            
        else:
            text_output = f"😃 {output} review"
            color = 'success'
    
    # if textarea box is empty
    else:
        visible = 'hidden'
        
    
    
    return text_output, color, {"visibility" : visible}