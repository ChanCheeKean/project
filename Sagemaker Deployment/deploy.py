import os
import boto3
import tarfile
import pandas as pd
from tqdm import tqdm
from sagemaker.pytorch import PyTorchModel
import sagemaker

### CONFIG
endpoint_name = 'test-model-v2'
s3_model_dir = ""
arn_role = ""
instance_type = 'ml.g4dn.xlarge'
torch_version = "1.12.0"
py_version = "py38"
initial_instance_count = 2
s3 = boto3.Session().client("s3")
file_name = os.path.join("./model.tar.gz")


### Step 1: file compression and uploading to s3 bucket
def build_tarfile(dir, files_to_add_and_rename):
    with tarfile.open(os.path.join(dir, "model.tar.gz"), "w:gz") as tar:
        for f_path, new_f_path in files_to_add_and_rename.items():
            tar.add(f_path, arcname=new_f_path)

# files to be compressed as tar
files_to_add_and_rename = {
    "models/" : "models/",
    "inference.py" : "code/inference.py",
    "requirements.txt": "code/requirements.txt",
}
build_tarfile('./', files_to_add_and_rename)

# Uploading tarfile to s3 bucket
file_size = os.stat(file_name).st_size
with tqdm(total=file_size, unit="B", unit_scale=True, desc=file_name, position=0, leave=True) as pbar:
    s3.upload_file(
        Filename=file_name,
        Bucket=s3_model_dir.split("//")[-1].split("/")[0],
        Key="/".join(s3_model_dir.split("//")[-1].split("/")[1:]) + "model.tar.gz",
        Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
    )


### Step 2: Build sagemaker pytorch model by refering to the correct role and s3 model
pytorch_model = PyTorchModel(
  model_data=os.path.join(s3_model_dir, "model.tar.gz"),
  role=arn_role,
  entry_point="inference.py",
  framework_version=torch_version,
  py_version=py_version,
)

### Step 3a: Register pytorch model as Sagemaker Endpoint
predictor = pytorch_model.deploy(
  instance_type=instance_type,
  endpoint_name=endpoint_name,
  initial_instance_count=initial_instance_count
)

### Step 3b: Deploy pytorch model as Batch Transform
pytorch_model.register(
    content_types=["application/jsonlines"],
    response_types=["application/json"],
    inference_instances=[instance_type],
    transform_instances=[instance_type],
    model_package_name=endpoint_name,
)

### Step 4: Trigger batch transform job
batch_input_path = f""
batch_output_path = f""

df = pd.read_csv(
    "https://raw.githubusercontent.com/ChanCheeKean/datasets/main/nlp/amazonreviews.tsv", 
    sep='\t'
).sample(1000)[['review', 'label']]

for i in range(0, len(df), 100):
    df.iloc[i : i + 100, :].to_json(f'{batch_input_path}/batch_{i}.json', orient='records', lines=True)

model_arn = 'arn:aws:sagemaker:us-east-1:852288348919:model-package/test-model-v2'
model = sagemaker.ModelPackage(
    role=arn_role,
    model_package_arn=model_arn,
    sagemaker_session=sagemaker.Session()
)

transformer = model.transformer(
    instance_count=1,
    instance_type=instance_type,
    strategy='MultiRecord',
    assemble_with='Line',
    output_path=batch_output_path,
    accept='application/jsonlines',
    # max_concurrent_transforms=0,
    max_payload=100,
    )

transformer.transform(
    data=batch_input_path,
    content_type='application/jsonlines',
    split_type="Line",
    join_source="Input",
    # output_filter="$['label', 'SageMakerOutput']",
    # model_client_config={"InvocationsMaxRetries": 0, "InvocationsTimeoutInSeconds": 100,}
)