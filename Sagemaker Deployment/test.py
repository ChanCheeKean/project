import json
import boto3
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import sagemaker

# model testing
tokenizer = AutoTokenizer.from_pretrained('./models/tokenizer/')
model = AutoModelForSequenceClassification.from_pretrained('./models/predictor/')
text = ['The food is surprisingly good!', 'Yuck! The food is shitty!']
encoded_input = tokenizer(text, return_tensors='pt', padding=True)
output = model(**encoded_input)
scores = softmax(output[0].detach().numpy())
labels = ['anger', 'joy', 'optimism', 'sadness']
final_label = [{x : y} for score in scores for x, y in zip(labels, score)]


# local inference test
from inference import *
input = json.dumps(['The food is surprisingly good!', 'Yuck! The food is shitty!'])
model = model_fn("./")
data = input_fn(input, "application/json")
predictions = predict_fn(data, model)
result = json.loads(output_fn(predictions, accept=None))


# sagemaker endpoint test
endpoint_name = 'test-model-v1'
payload = json.dumps(['The food is surprisingly good!', 'Yuck! The food is shitty!'])
response = boto3.client("runtime.sagemaker", region_name="us-east-1")\
    .invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=payload
    )
result = json.loads(response["Body"].read().decode())
print(result)