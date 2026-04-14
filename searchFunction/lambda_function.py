import boto3
import requests
from requests_aws4auth import AWS4Auth
import json

region = 'us-east-1'
service = 'es'

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    region,
    service,
    session_token=credentials.token
)

host = 'search-kp-search-public-z24bcdoa5cpwqwuamylxoxr744.us-east-1.es.amazonaws.com'
index = 'mygoogle'
datatype = '_doc'

headers = {"Content-Type": "application/json"}

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        for record in event['Records']:

            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']

            obj = s3.get_object(Bucket=bucket, Key=key)
            body = obj['Body'].read().decode('utf-8')

            url = f'https://{host}/{index}/{datatype}/{key}'

            document = {
                "Body": body
            }

            r = requests.put(url, auth=awsauth, json=document, headers=headers)

            print("Uploaded:", key, "Response:", r.text)

        return {
            "statusCode": 200,
            "body": "Success"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }