from boto3.dynamodb.conditions import Key, Attr

import boto3
import json
import os
import uuid
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

    if event['headers'].get('content-type', None) != 'application/json' and event['headers'].get('Content-Type', None) != 'application/json':
        return respond(415, {})

    body = json.loads(event['body'])

    response = table.query(
        KeyConditionExpression=Key('id').eq(event['pathParameters']['id'])
    )

    items = response['Items']
    if len(items) == 0:
        return respond(404, None)

    person = response['Items'][0]

    if not 'messages' in person:
        person['messages'] = []

    person['messages'] += [{ 'id': str(uuid.uuid4()), 'message': body['message'] }]

    table.update_item(
        Key={
            'id': person['id']
        },
        UpdateExpression='SET messages = :messages',
        ExpressionAttributeValues={
            ':messages': person['messages']
        }
    )

    # TODO sure would be nice to have a Location header and a 201 response

    return respond(None, person['messages'][-1])
