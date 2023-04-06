import json

def predict(items):
    result = items
    return result
    # endpoint_name = 'sklearn-local-ep2022-10-31-18-30-39'
    # runtime_client = boto3.client('sagemaker-runtime')
    
    # request_body = {"Input": items}
    
    # data = json.loads(json.dumps(request_body))
    # payload = json.dumps(data)
    
    # response = runtime_client.invoke_endpoint(
    #     EndpointName=endpoint_name,
    #     ContentType="application/json",
    #     Body=payload)
    # result = json.loads(response['Body'].read().decode())
    
    # return result['Output']
    