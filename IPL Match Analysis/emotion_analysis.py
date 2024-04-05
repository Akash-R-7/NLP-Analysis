import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, QuantoConfig, pipeline
import plotly.express as px
import plotly.graph_objects as go


def load_emotion_model():    
    # load tokenizer and model, create trainer
    model_name = "emotion-english-distilroberta-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    quantization_config = QuantoConfig(weights="int8")
    quantized_model = AutoModelForSequenceClassification.from_pretrained(model_name, quantization_config=quantization_config)

    return (tokenizer, quantized_model)


def classify_emotions(quantized_model, tokenizer, comments):
    classifier = pipeline("text-classification", model=quantized_model, tokenizer=tokenizer, top_k=None)
    preds = classifier(comments)
    return preds


def form_df(comments, preds):
    labels = []
    scores = []

    emot_dt = {'anger':0, 'disgust':0, 'fear':0, 'joy':0, 'neutral':0, 'sadness':0, 'surprise':0}
    # extract scores (as many entries as exist in pred_texts)
    for i in range(len(preds)):

        pred_label = preds[i][0]['label']
        pred_score = preds[i][0]['score']

        if pred_label == 'neutral':
            if pred_score >= 0.9:
                scores.append(pred_score)
                labels.append(pred_label)
            else:
                secondmost_label = preds[i][1]['label']
                secondmost_score = preds[i][1]['score']
                scores.append(secondmost_score)
                labels.append(secondmost_label) # second most prob emotion
        else:
            scores.append(pred_score)
            labels.append(pred_label)


    # Create DataFrame with texts, predictions, labels, and scores
    op_df = pd.DataFrame(list(zip(comments, labels, scores)), columns=['text', 'label','score'])
    return op_df




def plot_histogram(op_df):
    fig = px.histogram(op_df, x='label',
                   labels={'label':'Emotion'},
                   color='label',
                   color_discrete_sequence=px.colors.qualitative.G10,
            
                   )
    return fig



def plot_pie(op_df):
    emot_ct = {'fear':0, 'sadness':0, 'surprise':0, 'neutral':0, 'anger':0, 'disgust':0, 'joy':0}
    for emot in list(op_df['label']):
        emot_ct[emot] += 1

    fig = go.Figure(data=[go.Pie(labels=list(emot_ct.keys()), values=list(emot_ct.values()), 
                             textinfo='label+percent',
                             insidetextorientation='radial',
                              hole=0.3,
                            #   title="Public emotions on Reddit"
                              )])
    fig.update_layout(width=500, height=500)

    return fig



