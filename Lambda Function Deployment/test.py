import boto3
import json

client = boto3.client('lambda')
payload = {"key1": 111, "key2": 999}
response = client.invoke(
    FunctionName='test-image-dev',
    InvocationType='RequestResponse',
    Payload=json.dumps(payload)
    )
payload = response["Payload"].read().decode()
result = json.loads(json.loads(payload)['body'])
print(result)