import os
import logging
import json
import pandas as pd
from scipy.special import softmax
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
logger = logging.getLogger()

def model_fn(model_dir):
    '''Loading Model from saved directory'''

    logger.info(f"Loading model")
    tokenizer = AutoTokenizer.from_pretrained(os.path.join(model_dir, "./models/tokenizer/"))
    model = AutoModelForSequenceClassification.from_pretrained(os.path.join(model_dir, './models/predictor/'))
    return {'tokenizer': tokenizer, 'predictor': model}

def input_fn(request_body, content_type):
    '''Loading Data from User Input and serialize into list'''

    logger.info("Deserializing the input data")
    if content_type == "application/json":
        data = pd.read_json(request_body, orient="records", lines=True)
    elif content_type == "text/plain":
        data = pd.DataFrame({'text' : json.loads(request_body)})
    elif content_type == "text/csv":
        data = pd.read_csv(request_body)
    else:
        raise Exception(f"Requested unsupported ContentType in content_type: {content_type}")
    return data

def predict_fn(data, model):
    '''Generating Prediction for de-serialized data'''

    logger.info("Generating predictions")
    encoded_input = model['tokenizer'](data.iloc[:, 0].tolist(), return_tensors='pt', padding=True)
    output = model['predictor'](**encoded_input)
    scores = softmax(output[0].detach().numpy())
    labels = ['anger', 'joy', 'optimism', 'sadness']
    pred_list = [{x : str(y) for x, y in zip(labels, score)} for score in scores]
    data['result'] = pred_list
    return data

def output_fn(prediction_output, accept):
    '''Serialize generated ouput and return to user'''
    logger.info("Serializing Output")
    return prediction_output.to_json(orient="records", lines=True)
    # return json.dumps(pred_list)
