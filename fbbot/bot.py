import json
from pprint import pprint
import requests
import uuid

from django.contrib.staticfiles.templatetags.staticfiles import static

class Bot:
   def __init__(self,FB_PAGE_TOKEN,BASE_URL):
      self.FB_PAGE_TOKEN = FB_PAGE_TOKEN
      self.BASE_URL = BASE_URL
      self.message_type_functions = { 'optin': self.receivedAuthentication,
                                      'message' : self.receivedMessage,
                                      'delivery': self.receivedDeliveryConfirmation,
                                      'postback': self.receivedPostback,
                                      'read': self.receivedMessageRead,
                                      'account_linking': self.receivedAccountLink,
                                    }

   def get_user_info(self,fbid):
      user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
      user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':self.FB_PAGE_TOKEN}
      user_details = requests.get(user_details_url, user_details_params).json()
      pprint (user_details)
      return user_details

   def callSendAPI(self,msg_data):
      post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+self.FB_PAGE_TOKEN 
      pprint(post_message_url)
      status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=json.dumps(msg_data))
      status_body=status.json()
      if status.status_code == 200 :
         recipientId = status_body['recipient_id']
         if 'message_id' in status_body:
            messageId = status_body['message_id']
            pprint("Successfully sent message with id "+messageId+" to recipient "+recipientId)
         else:
            pprint("Successfully called Send API for recipient "+recipientId)
      else:
         pprint(status_body)

   def receivedAuthentication(self,message):
      senderID = message['sender']['id']
      recipientID = message['recipient']['id']
      timeOfAuth = message['timestamp']
      passThroughParam = message['optin']['ref']
      pprint("Received authentication for user "+senderID+" and page "+recipientID+" with pass "+"through param '"+passThroughParam+"' at "+repr(timeOfAuth))
      self.sendTextMessage(senderID, "Authentication successful")

   def receivedMessage(self,message):
      senderID = message['sender']['id']
      recipientID = message['recipient']['id']
      timeOfMessage = message['timestamp']
      received_message = message['message']
      pprint("Received message for user "+senderID+" and page "+recipientID+" at "+repr(timeOfMessage)+" with message:")
      #pprint(message)
      #pprint(received_message)
      isEcho = received_message['is_echo'] if 'is_echo' in received_message else False
      messageAttachments = received_message['attachments'] if 'attachments' in received_message else False
      messageText = received_message['text'] if 'text' in received_message else False
      quickReply = received_message['quick_reply'] if 'quick_reply' in received_message else False
   
      if isEcho:
         self.receivedMessageEcho(received_message)
         return
   
      elif quickReply:
         self.receivedMessageQuickReply(received_message,senderID)
         return
   
      if messageText:
         self.receivedMessageText(messageText,senderID)
      elif messageAttachments:
         self.receivedMessageAttachments(senderID)

   def receivedMessageEcho(self,received_message):
      appId = received_message['app_id'] if 'app_id' in received_message else ""
      metadata = received_message['metadata'] if 'metadata' in received_message else ""
      messageId = received_message['mid'] if 'mid' in received_message else ""
      pprint("Received echo for message "+messageId+" and app "+appId+" with metadata "+metadata)

   def receivedMessageQuickReply(self,received_message,senderID):
      messageId = received_message['mid'] if 'mid' in received_message else ""
      quickReply = received_message['quick_reply'] if 'quick_reply' in received_message else False
      quickReplyPayload = quickReply['payload']
      pprint("Quick reply for message "+messageId+" with payload "+quickReplyPayload)
      self.sendTextMessage(senderID, "Quick reply tapped")

   def receivedMessageAttachments(self,messageAttachments,senderID):
      self.sendTextMessage(senderID, "Message with attachment received")

   def receivedMessageText(self,messageText,senderID):
      if messageText == 'image':
         self.sendImageMessage(senderID,"fbbot/python.png")
      elif messageText == 'gif':
         self.sendGifMessage(senderID,"fbbot/falling_down.gif")
      elif messageText == 'audio':
         self.sendAudioMessage(senderID,"fbbot/sample.mp3")
      #elif messageText == 'video':
      #   sendVideoMessage(senderID,"fbbot/animal.mp4")
      elif messageText == 'file':
         self.sendFileMessage(senderID,"fbbot/test.txt")
      elif messageText == 'button':
         self.sendButtonMessage(senderID)
      elif messageText == 'generic':
         self.sendGenericMessage(senderID)
      elif messageText == 'receipt':
         self.sendReceiptMessage(senderID)
      elif messageText == 'quick reply':
         self.sendQuickReply(senderID)
      elif messageText == 'read receipt':
         self.sendReadReceipt(senderID)
      elif messageText == 'typing on':
         self.sendTypingOn(senderID)
      elif messageText == 'typing off':
         self.sendTypingOff(senderID)
      elif messageText == 'account linking':
         self.sendAccountLinking(senderID)
      else:
         self.sendTextMessage(senderID, messageText)


   def receivedDeliveryConfirmation(self,message):
      #senderID = message['sender']['id']
      #recipientID = message['recipient']['id']
      pprint(message)
      delivery = message['delivery']
      messageIDs = delivery['mids']
      watermark = delivery['watermark']
      #secuenceNumber = delivery['seq']
      if messageIDs:
         for messageID in messageIDs:
            pprint("Received delivery confirmation for message ID: "+messageID)
      pprint("All message before "+repr(watermark)+" were delivered.")

   def receivedPostback(self,message):
      senderID = message['sender']['id']
      recipientID = message['recipient']['id']
      timeOfPostback = message['timestamp']
      payload = message['postback']['payload']
      pprint("Received postback for user "+senderID+" and page "+recipientID+" with payload '"+payload+"' "+"at "+repr(timeOfPostback))
      self.sendTextMessage(senderID, "Postback called")

   def receivedMessageRead(self,message):
      #senderID = message['sender']['id']
      #recipientID = message['recipient']['id']
      watermark = message['read']['watermark']
      sequenceNumber = message['read']['seq']
      pprint("Received message read event for watermark "+watermark+" and sequence number "+sequenceNumber)

   def receivedAccountLink(self,message):
      senderID = message['sender']['id'];
      #recipientID = message['recipient']['id'];
      status = message['account_linking']['status'];
      authCode = message['account_linking']['authorization_code'];
      pprint("Received account link event with for user "+senderID+" with status "+status+" and auth code "+authCode);

   def sendImageMessage(self,recipientId,static_img_url):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'message':{
            'attachment':{
               'type': "image",
               'payload': {
                  'url': self.BASE_URL+static(static_img_url)
               }
            }
         }
      }
      self.callSendAPI(msg_data)

   def sendGifMessage(self,recipientId,static_img_url):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'message':{
            'attachment':{
               'type': "image",
               'payload': {
                  'url': self.BASE_URL+static(static_img_url)
               }
            }
         }
      }
      self.callSendAPI(msg_data)

   def sendAudioMessage(self,recipientId,static_audio_url):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'message':{
            'attachment':{
               'type': "audio",
               'payload': {
                  'url': self.BASE_URL+static(static_audio_url)
               }
            }
         }
      }
      self.callSendAPI(msg_data)

   def sendVideoMessage(self,recipientId,static_video_url):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'message':{
            'attachment':{
               'type': "video",
               'payload': {
                  'url': self.BASE_URL+static(static_video_url)
               }
            }
         }
      }
      self.callSendAPI(msg_data)

   def sendFileMessage(self,recipientId,static_file_url):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'message':{
            'attachment':{
               'type': "file",
               'payload': {
                  'url': self.BASE_URL+static(static_file_url)
               }
            }
         }
      }
      self.callSendAPI(msg_data)

   def sendTextMessage(self,recipientId,messageText,metadata="DEVELOPER_DEFINED_METADATA"):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'message': {
            'text': messageText,
            'metadata': metadata
         }
      }
      self.callSendAPI(msg_data)

   def sendButtonMessage(self,recipientId):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'message':{
            'attachment':{
               'type': "template",
               'payload': {
                  'template_type': "button",
                  'text': "This is test text",
                  'buttons': [{
                     'type': "web_url",
                     'url': "https://www.oculus.com/en-us/rift/",
                     'title': "Open Web URL"
                  },{
                     'type': "postback",
                     'title': "Trigger Postback",
                     'payload': "DEVELOPER_DEFINED_PAYLOAD"
                  },{
                     'type': "phone_number",
                     'title': "Call Phone Number",
                     'payload': "+55555555555"
                  }] 
               }
            }
         }
      }
      self.callSendAPI(msg_data)

   def sendGenericMessage(self,recipientId):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'message': {
            'attachment': {
               'type': "template",
               'payload': {
                  'template_type': "generic",
                  'elements': [{
                     'title': "42",
                     'subtitle': "Next-generation guides",
                     'item_url': "https://en.wikipedia.org/wiki/The_Hitchhiker%27s_Guide_to_the_Galaxy",
                     'image_url': self.BASE_URL+static("fbbot/falling_down.gif"),
                     'buttons': [{
                        'type': "web_url",
                        'url': "https://en.wikipedia.org/wiki/The_Hitchhiker%27s_Guide_to_the_Galaxy",
                        'title': "Open Web URL"
                     }, {
                        'type': "postback",
                        'title': "Call Postback",
                        'payload': "Payload for first bubble",
                     }],
                  }, {
                     'title': "books",
                     'subtitle': "books collection",
                     'item_url': "https://www.books.com/",               
                     'image_url': self.BASE_URL+static("fbbot/books.png"),
                     'buttons': [{
                        'type': "web_url",
                        'url': "https://www.oculus.com/en-us/touch/",
                        'title': "Open Web URL"
                     }, {
                        'type': "postback",
                        'title': "Call Postback",
                        'payload': "Payload for second bubble",
                     }]
                  }]
               }
            }
         }
      }
      self.callSendAPI(msg_data)

   def sendReceiptMessage(self,recipientId):
      receiptId = uuid.uuid4().hex.upper()
      msg_data = {
         'recipient': {
           'id': recipientId
         },
         'message':{
            'attachment': {
               'type': "template",
               'payload': {
                  'template_type': "receipt",
                  'recipient_name': "Peter Chang",
                  'order_number': receiptId,
                  'currency': "USD",
                  'payment_method': "Visa 1234",        
                  'timestamp': "1428444852", 
                  'elements': [{
                     'title': "Surprise package",
                     'subtitle': "Includes: mistery item1, item2, item3",
                     'quantity': 1,
                     'price': 599.00,
                     'currency': "USD",
                     'image_url': self.BASE_URL+static("fbbot/surprise_pkg.png")
                  }, {
                     'title': "Books collection",
                     'subtitle': "Paper version",
                     'quantity': 1,
                     'price': 99.99,
                     'currency': "USD",
                     'image_url': self.BASE_URL+static("fbbot/books.png")
                  }],
                  'address': {
                     'street_1': "1 Hacker Way",
                     'street_2': "",
                     'city': "Menlo Park",
                     'postal_code': "94025",
                     'state': "CA",
                     'country': "US"
                  },
                  'summary': {
                     'subtotal': 698.99,
                     'shipping_cost': 20.00,
                     'total_tax': 57.67,
                     'total_cost': 626.66
                  },
                  'adjustments': [{
                     'name': "New Customer Discount",
                     'amount': -50
                  }, {
                     'name': "$100 Off Coupon",
                     'amount': -100
                  }]
               }
            }
         }
      }
      self.callSendAPI(msg_data)

   def sendQuickReply(self,recipientId):
      msg_data = {
         'recipient': {
           'id': recipientId
         },
         'message':{
            'text': "What's your favorite movie genre?",
            'quick_replies': [
               {
                  "content_type":"text",
                  "title":"Action",
                  "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_ACTION"
               },
               {
                  "content_type":"text",
                  "title":"Comedy",
                  "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_COMEDY"
               },
               {
                  "content_type":"text",
                  "title":"Drama",
                  "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_DRAMA"
               }
            ]
         }
      }
      self.callSendAPI(msg_data)

   def sendReadReceipt(self,recipientId):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'sender_action': "mark_seen"
      }
      self.callSendAPI(msg_data)

   def sendTypingOn(self,recipientId):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'sender_action': "typing_on"
      }
      self.callSendAPI(msg_data)

   def sendTypingOff(self,recipientId):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'sender_action': "typing_off"
      }
      self.callSendAPI(msg_data)

   def sendAccountLinking(self,recipientId):
      msg_data = {
         'recipient': {
            'id': recipientId
         },
         'message': {
            'attachment': {
               'type': "template",
               'payload': {
                  'template_type': "button",
                  'text': "Welcome. Link your account.",
                  'buttons':[{
                     'type': "account_link",
                     'url': self.BASE_URL+"/admin"
                  }]
               }
            }
         }
      }
      self.callSendAPI(msg_data)
