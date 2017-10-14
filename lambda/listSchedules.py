from boto3.dynamodb.conditions import Key, Attr

import boto3
import json
import os
from decimal import Decimal

class fakefloat(float):
    def __init__(self, value):
        self._value = value
    def __repr__(self):
        return str(self._value)

def defaultencode(o):
    if isinstance(o, Decimal):
        # Subclass float with custom repr?
        return fakefloat(o)
    raise TypeError(repr(o) + " is not JSON serializable")


print('Loading function')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE'])


def respond(code, res=None):
    return {
        'statusCode': code if code else '200',
        'body': None if code else json.dumps(res, default=defaultencode),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    # print("Received event from apigw: " + json.dumps(event, indent=2))

    response = table.query(
        KeyConditionExpression=Key('id').eq(event['pathParameters']['id'])
    )

    items = response['Items']
    if len(items) > 0:
        return respond(None, items[0].get('schedules', []))
    else:
        return respond(404, None)
