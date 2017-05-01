# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from pprint import pprint

#from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from bot import Bot

# Creating a Bot
myBot = Bot(settings.FB_PAGE_TOKEN, settings.BASE_URL)

# Create your views here.
@csrf_exempt
def bot(request):
   if request.method=='GET':
      if 'hub.verify_token' in request.GET and request.GET['hub.verify_token'] == settings.FB_VERIFY_TOKEN:
         return HttpResponse(request.GET['hub.challenge'])
      else:
         return HttpResponse("Hello World, webhook enable")
   if request.method=='POST':
      incoming_message = json.loads(request.body.decode('utf-8'))
      #pprint(incoming_message)
      if 'object' in incoming_message and incoming_message['object'] == 'page':
         for entry in incoming_message['entry']:
            for message in entry['messaging']:
               #pprint(message)
               for message_type in myBot.message_type_functions:
                  if message_type in message:
                     myBot.message_type_functions[message_type](message)
      return HttpResponse()
