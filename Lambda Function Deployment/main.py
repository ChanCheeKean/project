import pandas as pd
import json

def handler(event, context):

    # For API Gateway
    if "body" in event:
        event = json.loads(event["body"])
    
    p1 = event["key1"]
    p2 = event["key2"]
    
    result = {
        "sum": p1 + p2,
        "substract": p1 - p2,
    }

    # For API Gateway
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(result),
    }