import os
import boto3

from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(os.environ.get('DATABASE_NAME'))

response = table.scan()
items = response['Items']
print(items)
