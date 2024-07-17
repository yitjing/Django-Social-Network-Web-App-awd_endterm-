#references from coursera and class lecturer and geeks for geeks
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
	#call when websocket connection is active
	def connect(self):
		#receive room name from the url route
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name
		
		#Join room group
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)
		
		self.accept()
		
	#call when websocket connection is close
	def disconnect(self, close_code):
		#leave the chat room
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)
	
	# call when the websocket receive messages from the client
	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		userName = text_data_json['userName']
		
		#send message to chat room
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message,
				'userName': userName
			}
		)
		
	# receive message from the room group
	# allows real time chat to happen
	def chat_message(self, event):
		message = event['message']
		userName = event['userName']
		
		#send the client message to webSocket
		self.send(text_data=json.dumps({
			'message':message,
			'userName': userName
		}))
