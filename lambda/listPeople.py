import boto3
import json
import os

print('Loading function')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE'])


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    response = table.scan()
    items = response['Items']

    return respond(None, items)
