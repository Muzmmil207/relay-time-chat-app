import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
        self.group_name = "chat_%s" % self.chat_box_name
        async_to_sync(
            self.channel_layer.group_add
        )(
            self.group_name,
            self.channel_name
        )
        self.accept()


    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(
            self.channel_layer.group_send
        )(
            "chat_%s" % text_data_json['username'],
            {
                'type': 'chat_message',
                'message': message,
            }
        )


    def chat_message(self, event):

        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'mes',
            'message': message,
        }))







