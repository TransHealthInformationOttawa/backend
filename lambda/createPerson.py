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

    if event['headers'].get('Content-Type', None) != 'application/json':
        return respond(415, {})

    body = json.loads(event['body'])

    name = body.get('name', None)
    if name != None:
        name = name.strip()

    phone = body.get('phone', None)
    if phone != None:
        phone = phone.strip()

    person = {
        'id': str(uuid.uuid4()),
        'name': name,
        'enabled': phone != None and phone != '',
        'phone': phone,
        'schedules': [],
        'messages': [],
    }

    table.put_item(
        Item=person,
    )

    # TODO sure would be nice to have a Location header and a 201 response

    return respond(None, person)
