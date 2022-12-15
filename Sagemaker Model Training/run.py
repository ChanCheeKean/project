from sagemaker.pytorch.estimator import PyTorch
from sagemaker import get_execution_role

# https://github.com/aletheia/mnist_pl_sagemaker
torch_estimator = PyTorch(
    base_job_name="test-pytorch-run",
    entry_point="train.py",
    framework_version="1.12.0",
    py_version = "py38",
    dependencies=["requirements.txt"], # ['utils', 'configs']
    instance_count=1,
    instance_type="ml.m5.large",
    use_spot_instances=True,
    max_wait=600,
    max_run=600,
    role="arn:aws:iam::852288348919:role/sagemaker",
    hyperparameters={
        "model_dir": "s3://dxi-models/archive/",
    },
)

### Launch Training job
torch_estimator.fit()

### retract last model
import boto3
sm_client = boto3.client("sagemaker")
training_job_name = torch_estimator.latest_training_job.name
job_desc = sm_client.describe_training_job(TrainingJobName=training_job_name)
model_artifact = job_desc["ModelArtifacts"]["S3ModelArtifacts"]
print(f"Training job name: {training_job_name}")
print(f"Model storage location: {model_artifact}")