from send_message import upcomingMessages

adrian = {
  "id" : "22313131",
  "name" : "Adrian",
  "lastMessageSent" : "3",
  "enabled" : "true"
  ,
  "phone" : "+12267482821",
  "schedules" : [{
    "id" : "1",
    "dayOfWeek": 1, # Monday
    "hour": 12,
    "minute": 30
  },
  {
    "id" : "2",
    "dayOfWeek": 2, # Tuesday
    "hour": 12,
    "minute": 30
  }
  ,{
    "id" : "3",
    "dayOfWeek": 6, # Saturday
    "hour": 12,
    "minute": 30
  }
  ,{
    "id" : "4",
    "dayOfWeek": 6, # Saturday
    "hour": 17,
    "minute": 50
  }
  ,{
    "id" : "5",
    "dayOfWeek": 6, # Saturday
    "hour": 17,
    "minute": 46
  }
  ,{
    "id" : "6",
    "dayOfWeek": 6, # Saturday
    "hour": 17,
    "minute": 12
  }
  ,{
    "id" : "7",
    "dayOfWeek": 6, # Saturday
    "hour": 15,
    "minute": 6
  }
  ,{
    "id" : "8",
    "dayOfWeek": 6, # Saturday
    "hour": 15,
    "minute": 0
  }
  ,{
    "id" : "9",
    "dayOfWeek": 6, # Saturday
    "hour": 16,
    "minute": 7
  }],
  "messages" : [
    {
      "id" : "1",
      "message" : "You're awesome"
    },
    {
      "id" : "2",
      "message" : "You're great"
    },
    {
      "id" : "3",
      "message" : "You're super"
    },
    {
      "id" : "4",
      "message" : "You're special"
    },
    {
      "id" : "5",
      "message" : "You're fantastic"
    },
    {
      "id" : "6",
      "message" : "You're loved"
    },
    {
      "id" : "7",
      "message" : "You're fun"
    },
    {
      "id" : "8",
      "message" : "You're sweet"
    },
  ]
}

evan = {
  "id" : "3257535",
  "name" : "Evan",
  "lastMessageSent" : "0",
  "enabled" : "true"
  ,
  "phone" : "+12267482821",
  "schedules" : [{
    "id" : "1",
    "year": 2017,
    "dayOfWeek": 1, # Monday
    "dayOfMonth": 14
  },
  {
    "id" : "2",
    "year": 2017,
    "dayOfWeek": 2, # Tuesday
    #"month": null,
    #"dayOfMonth": null,
    "hour": 12,
    "minute": 30
  }
  ,{
    "id" : "3",
    "year": 2018,
    "dayOfWeek": 6, # Saturday
    "hour": 12,
    "minute": 30
  }
  ,{
    "id" : "4",
    "dayOfWeek": 6, # Saturday
    "month": 2,
    "hour": 13,
    "minute": 30
  }
  ,{
    "id" : "5",
    "dayOfMonth": 2,
    "hour": 15,
    "minute": 16
  }
  ,{
    "id" : "6",
    "minute": 0
  }
  ,{
    "id" : "7",
    "dayOfMonth": 6, # Saturday
    "hour": 15,
    "minute": 6
  }
  ,{
    "id" : "8",
    "dayOfWeek": 6, # Saturday
    "month": 4,
    "hour": 16,
    "minute": 15
  }
  ,{
    "id" : "9",
    "month": 2,
    "dayOfMonth": 29
  }],
  "messages" : [
    {
      "id" : "1",
      "message" : "You gots this!"
    },
    {
      "id" : "2",
      "message" : "Keep up the great work!"
    }
  ]
}


upcomingMessages(evan)
upcomingMessages(evan)
upcomingMessages(adrian)
upcomingMessages(adrian)
upcomingMessages(adrian)

