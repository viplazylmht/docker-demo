import os
from datetime import datetime
import time
import threading
import json

from kafka.errors import KafkaError

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer

KAFKA_CLUSTER_DOMAIN = os.getenv('KAFKA_CLUSTER_DOMAIN', 'kafka')
KAFKA_CLUSTER_PORT = os.getenv('KAFKA_CLUSTER_PORT', 9092)
bootstrap_servers=f"{KAFKA_CLUSTER_DOMAIN}:{KAFKA_CLUSTER_PORT}"

print(f"Producer will send data to `{bootstrap_servers}`") 

CONSUMER_KEY = os.getenv('CONSUMER_KEY', "")
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET', "")
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', "")
ACCESS_SECRET = os.getenv('ACCESS_SECRET', "")

def stream_tweets(topic, tracks):
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    while True:
        listener = ListenerTS(topic=topic)
        stream = Stream(auth, listener)
        stream.filter(track=tracks, stall_warnings=True, languages= ["en"])

class ListenerTS(StreamListener):

    def __init__(self, topic):
        self.producer = KafkaProducer(bootstrap_servers=f"{KAFKA_CLUSTER_DOMAIN}:{KAFKA_CLUSTER_PORT}") #Same port as your Kafka server
        self.topic_name = topic

        super().__init__()

    def on_data(self, raw_data):
            json_data = json.loads(str.encode(raw_data))
            self.producer.send(self.topic_name, str.encode(json.dumps(dict(id=json_data['id'], text=json_data['text'], timestamp_ms=json_data['timestamp_ms']))))
            return True

topics = [r[:-1] for r in open('topics.txt', 'rt').readlines()]

#topic = topics[0]

# for topic in topics:

#     print(f"Starting listener on topic: `{topic}`")

#     stream_tweets(topic, [topic,])

producers=[]

for topic in topics:
   print(f"Starting listener on topic: `{topic}`")
   producer = threading.Thread(target=stream_tweets, args=(topic, [topic,]))
   producer.start()
   producers.append(producer)

print("Done. Infinity loop now....")

while True:
   pass

