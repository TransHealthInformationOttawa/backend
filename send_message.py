from twilio.rest import Client
from boto3.dynamodb.conditions import Key, Attr
import boto3
import datetime
import os
import time
import uuid

dynamodb = boto3.resource('dynamodb')

# Assumptions about the schedule of the (lamba) scheduler that periodically runs the code
script_interval_minutes = 60
error_buffer_minutes = 2

def minutesDifference(d1, d2):
  d1_ts = time.mktime(d1.timetuple())
  d2_ts = time.mktime(d2.timetuple())

  # They are now in seconds, subtract and then divide by 60 to get minutes.
  return int(d2_ts-d1_ts) / 60

def upcomingMessages(person):
  if not "messages" in person:
    return
  if len(person["messages"]) == 0:
    return

  now = datetime.datetime.now()
  for index in range(len(person["schedules"])):
    schedule = person["schedules"][index]

    year = now.year
    if "year" in schedule:
      if schedule["year"] != year:
        continue

    dayOfWeek = now.today().weekday() + 1 # We are using 1 = Monday, Python returns 0 = Monday
    if "dayOfWeek" in schedule:
      if schedule["dayOfWeek"] != dayOfWeek:
        continue

    month = now.month
    if "month" in schedule:
      if schedule["month"] != month:
        continue

    dayOfMonth = now.day
    if "dayOfMonth" in schedule:
      if schedule["dayOfMonth"] != dayOfMonth:
        continue

    hour = now.hour
    if "hour" in schedule:
      hour = schedule["hour"]
    
    minute = now.minute
    if "minute" in schedule:
      minute = schedule["minute"]

    time = datetime.datetime(year,month,dayOfMonth,hour,minute)
    delta_minutes = minutesDifference(now,time)
    if 0 <= delta_minutes and delta_minutes < script_interval_minutes + error_buffer_minutes:
      print 'Current schedule : (', schedule["id"], ") ", time
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
      print person["messages"][indexOfNextMessage]["message"]

def schedule(datetime):
  return {
    'id': str(uuid.uuid4()),
    'year': datetime.year,
    'month': datetime.month,
    'dayOfMonth': datetime.day,
    'hour': datetime.hour,
    'minute': datetime.minute
  }

def scheduleSomeMessagesSoon(person):

  table = dynamodb.Table(os.environ.get('DATABASE_NAME'))

  if not 'schedules' in person:
      person['schedules'] = []

  now = datetime.datetime.now()
  very_soon = now + datetime.timedelta(0, 10)
  soon = now + datetime.timedelta(0,60 * 10)
  in_an_hour = now + datetime.timedelta(0, 60 * 60)
  person['schedules'] += [schedule(very_soon)]
  person['schedules'] += [schedule(soon)]
  person['schedules'] += [schedule(in_an_hour)]

  table.update_item(
    Key={
        'id': person['id']
    },
    UpdateExpression='SET schedules = :schedules',
    ExpressionAttributeValues={
        ':schedules': person['schedules']
    }
  )

def getAllPeople():
  table = dynamodb.Table(os.environ.get('DATABASE_NAME'))
  response = table.scan()
  return response['Items']


def checkAllPeopleForMessages():
  people = getAllPeople()

  for index in range(len(people)):
    scheduleSomeMessagesSoon(people[index])

  time.sleep(5)

  for index in range(len(people)):
    upcomingMessages(people[index])
