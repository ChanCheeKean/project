import json
import boto3
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import sagemaker


### model testing
tokenizer = AutoTokenizer.from_pretrained('./models/tokenizer/')
model = AutoModelForSequenceClassification.from_pretrained('./models/predictor/')
text = ['The food is surprisingly good!', 'Yuck! The food is shitty!']
encoded_input = tokenizer(text, return_tensors='pt', padding=True)
output = model(**encoded_input)
scores = softmax(output[0].detach().numpy())
labels = ['anger', 'joy', 'optimism', 'sadness']
final_label = [{x : y} for score in scores for x, y in zip(labels, score)]


### local inference test
from inference import *
input = json.dumps(['The food is surprisingly good!', 'Yuck! The food is shitty!'])
model = model_fn("./")
data = input_fn(input, "text/plain")
predictions = predict_fn(data, model)
result = output_fn(predictions, accept=None)
print(result)

### sagemaker endpoint test
endpoint_name = '<your-endpoint-name>'
payload = json.dumps(['The food is surprisingly good!', 'Yuck! This is awful'])
response = boto3.client("runtime.sagemaker", region_name="us-east-1")\
    .invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="text/plain",
        Body=payload
    )
result = response["Body"].read().decode()
print(result)

### split into batches
batch_input_path = "<input-json-folder>"
batch_output_path = "<output-json-folder>"

df = pd.read_csv(
    "https://raw.githubusercontent.com/ChanCheeKean/datasets/main/nlp/amazonreviews.tsv", 
    sep='\t'
).sample(100)[['review', 'label']]
for i in range(0, len(df), 10):
    df.iloc[i : i + 10, :].to_json(f'{batch_input_path}/batch_{i}.json', orient='records', lines=True)


### sagemaker batch transform job
arn_role = "<your-sagemaker-role>"
model_arn = "<your-model-arn-,arketplace>"
model = sagemaker.ModelPackage(
    role=arn_role,
    model_package_arn=model_arn,
    sagemaker_session=sagemaker.Session()
)

transformer = model.transformer(
    instance_count=2,
    instance_type='ml.g4dn.xlarge',
    strategy='MultiRecord',
    assemble_with='Line',
    output_path=batch_output_path,
    accept='application/json',
    # max_concurrent_transforms=0,
    max_payload=100,
    )

transformer.transform(
    data=batch_input_path,
    content_type='application/json',
    split_type="Line",
    join_source="Input",
    output_filter="$['label', 'SageMakerOutput']",
    # model_client_config={"InvocationsMaxRetries": 0, "InvocationsTimeoutInSeconds": 100,}
)