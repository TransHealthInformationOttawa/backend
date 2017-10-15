from boto3.dynamodb.conditions import Key, Attr
import boto3
import datetime
import os
import re
import time
import uuid
import base64
import json
import urllib
from urllib import request, parse

TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
  checkAllPeopleForMessages()
  return {
      'statusCode': 200,
  }

# Assumptions about the schedule of the (lamba) scheduler that periodically runs the code
script_interval_minutes = 60
error_buffer_minutes = 2

def formatPhone(number):
  m = re.search('\+?1?-?\(?([1-9]\d{2})\)?-? ?(\d{3}) ?-?(\d{4})', number)
  if not m:
    return None
  return "+1" + m.group(1) + m.group(2) + m.group(3)

def sendSMS(number,message):
  number = os.environ.get('RECIPIENT_TELEPHONE', formatPhone(number))

  # insert Twilio Account SID into the REST API URL
  populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
  post_params = {"To": number, "From": os.environ['SENDER_TELEPHONE'], "Body": message}
 
  # encode the parameters for Python's urllib
  data = parse.urlencode(post_params).encode()
  req = request.Request(populated_url)
 
  # add authentication header to request based on Account SID + Auth Token
  authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
  base64string = base64.b64encode(authentication.encode('utf-8'))
  req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
 
  try:
    # perform HTTP POST request
    request.urlopen(req, data)
    #with request.urlopen(req, data) as f:
    # print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
  except Exception as e:
    # something went wrong!
    print(str(e))
    return
 
  print("SMS sent successfully!")

def minutesDifference(d1, d2):
  d1_ts = time.mktime(d1.timetuple())
  d2_ts = time.mktime(d2.timetuple())

  # They are now in seconds, subtract and then divide by 60 to get minutes.
  return int(d2_ts-d1_ts) / 60

def isSet(schedule,field):
  if field in schedule:
    if schedule[field] == '':
      return False
    if field != 'minute' and field != 'hour' and field == 0:
      return False
    return True
  else:
    return False

def upcomingMessages(person):
  if not "messages" in person:
    return
  if len(person["messages"]) == 0:
    return

  # TODO fix evil hack that puts everything in Eastern time
  now = datetime.datetime.now() + datetime.timedelta(0, 0, 0, 0, 0, -4)
  for index in range(len(person["schedules"])):
    schedule = person["schedules"][index]
  
    year = now.year
    if isSet(schedule, "year"):
      if schedule["year"] != year:
        continue

    dayOfWeek = now.today().weekday() + 1 # We are using 1 = Monday, Python returns 0 = Monday
    if isSet(schedule, "dayOfWeek"):
      if schedule["dayOfWeek"] != dayOfWeek:
        continue

    month = now.month
    if isSet(schedule, "month"):
      if schedule["month"] != month:
        continue

    dayOfMonth = now.day
    if isSet(schedule, "dayOfMonth"):
      if schedule["dayOfMonth"] != dayOfMonth:
        continue

    hour = now.hour
    if isSet(schedule, "hour"):
      hour = schedule["hour"]
    
    minute = now.minute
    if isSet(schedule, "minute"):
      minute = schedule["minute"]

    time = datetime.datetime(year,month,dayOfMonth,hour,minute)
    delta_minutes = minutesDifference(now,time)
    if 0 <= delta_minutes and delta_minutes < script_interval_minutes + error_buffer_minutes:
      # print('Current schedule : (', schedule["id"], ") ", time)
      indexOfLastMessage = 0
      idOfLastMessgeSend = 0
      if "lastMessageSent" in person:
        idOfLastMessgeSend = person["lastMessageSent"]
      for index in range(len(person["messages"])):
        if person["messages"][index]["id"] == idOfLastMessgeSend:
          indexOfLastMessage = index
      indexOfNextMessage = indexOfLastMessage + 1
      if (indexOfNextMessage == len(person["messages"])):
        indexOfNextMessage = 0
      person["lastMessageSent"] = person["messages"][indexOfNextMessage]["id"]
      # print(person["messages"][indexOfNextMessage]["message"])
      sendSMS(person["phone"],person["messages"][indexOfNextMessage]["message"])
      table = dynamodb.Table(os.environ.get('DATABASE_NAME'))
      table.update_item(
        Key={
          'id': person["id"]
        },
        UpdateExpression='SET lastMessageSent = :val1',
        ExpressionAttributeValues={
          ':val1': person["messages"][indexOfNextMessage]["id"]
        }
      )


def getAllPeople():
  table = dynamodb.Table(os.environ.get('DATABASE_NAME'))
  response = table.scan()
  return response['Items']


def checkAllPeopleForMessages():
  people = getAllPeople()
  for index in range(len(people)):
    upcomingMessages(people[index])
