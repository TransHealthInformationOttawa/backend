from boto3.dynamodb.conditions import Key, Attr

import boto3
import json
import os

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

    response = table.query(
        KeyConditionExpression=Key('id').eq(event['pathParameters']['id'])
    )

    items = response['Items']
    if len(items) > 0:
        schedules = items[0].get('schedules', [])

        for schedule in schedules:
            if schedule['id'] == event['pathParameters']['scheduleID']:
                return respond(None, schedule)

    return respond(404, None)
