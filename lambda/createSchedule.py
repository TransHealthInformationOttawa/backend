from boto3.dynamodb.conditions import Key, Attr

import boto3
import json
import os
import uuid

print('Loading function')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE'])


def respond(code, res=None):
    return {
        'statusCode': code if code else '200',
        'body': None if code else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    # print("Received event from apigw: " + json.dumps(event, indent=2))

    body = json.loads(event['body'])

    response = table.query(
        KeyConditionExpression=Key('id').eq(event['pathParameters']['id'])
    )

    items = response['Items']
    if len(items) == 0:
        return respond(404, None)

    person = response['Items'][0]

    if not 'schedules' in person:
        person['schedules'] = []

    person['schedules'] += [{
        'id': str(uuid.uuid4()),
        'year': body.get('year', None),
        'dayOfWeek': body.get('dayOfWeek', None),
        'month': body.get('month', None),
        'dayOfMonth': body.get('dayOfMonth', None),
        'hour': body.get('hour', None),
        'minute': body.get('minute', None),
    }]

    table.update_item(
        Key={
            'id': person['id']
        },
        UpdateExpression='SET schedules = :schedules',
        ExpressionAttributeValues={
            ':schedules': person['schedules']
        }
    )

    # TODO sure would be nice to have a Location header and a 201 response

    return respond(None, person['schedules'][-1])
