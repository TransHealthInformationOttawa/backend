import os
from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID']
# Your Auth Token from twilio.com/console
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)

message = client.messages.create(
  to=os.environ['RECIPIENT_TELEPHONE'],
  from_=os.environ['SENDER_TELEPHONE'],
  body="When's lunch?")

print(message.sid)
