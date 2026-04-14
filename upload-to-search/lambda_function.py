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
url = f'https://{host}/{index}/_search'

def lambda_handler(event, context):
    try:
        params = event.get('queryStringParameters') or {}
        term = params.get('q', '')

        query = {
            "size": 25,
            "query": {
                "multi_match": {
                    "query": term,
                    "fields": ["Title", "Author", "Date", "Body"]
                }
            }
        }

        r = requests.get(url, auth=awsauth, json=query)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": r.text
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }