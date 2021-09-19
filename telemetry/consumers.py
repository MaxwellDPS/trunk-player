from os import system
import re
import json
import logging
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from radio.models import System
from .telemetry import handleMessage

logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)

class TelemetryConsumer(WebsocketConsumer):
    def connect(self):
        try:
            recorder_uuid =  self.scope['url_route']["kwargs"]["recorder_uuid"]
        except:
            # setup fake channel so the javascript does not try and reconnect
            recorder_uuid = None
            self.close()

        # log.error('user %s connect %s=%s client=%s:%s', 
        #     message.user, tg_type, label, message['client'][0], message['client'][1])
    
            
        self.accept()
        self.recorder_uuid=recorder_uuid

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.recorder_uuid,
                self.channel_name
            )
        except (KeyError, System.DoesNotExist):
            pass

        
        # Leave room group
        

    # Receive message from WebSocket
    def receive(self, text_data):
        message = json.loads(text_data)
        tx_type = message["type"]
        try:           
            System.objects.get(recorder_uuid=self.recorder_uuid)
        except KeyError:
            log.error('no valid system found')
            return
       

        # conform to the expected message format.
        #try:
        log.error(f"Got {tx_type} Message")
        handleMessage(message, tx_type, self.recorder_uuid)
        #except ValueError:
       #     log.error("ws message isn't json text=%s", text_data)
       #     return
            
