from flair.models import TextClassifier
from flair.data import Sentence
sia = TextClassifier.load('en-sentiment')

def flair_prediction(x):
    sentence = Sentence(x)
    sia.predict(sentence)
    value, score = sentence.labels[0].value, sentence.labels[0].score
    return value, score

from kafka import KafkaConsumer
import json, threading, requests, os

KAFKA_CLUSTER_DOMAIN = os.getenv('KAFKA_CLUSTER_DOMAIN', 'kafka')
KAFKA_CLUSTER_PORT = os.getenv('KAFKA_CLUSTER_PORT', 9092)
bootstrap_servers=f"{KAFKA_CLUSTER_DOMAIN}:{KAFKA_CLUSTER_PORT}"

class ConsumerThread(threading.Thread):
    def __init__(self, topic, flair_pred):
        super().__init__()
        self.topic = topic
        self.is_stopped = False
        self.flair_pred = flair_pred
        self.url = 'https://tweettrenddemokafka.viplazy.repl.co/api/insert'

        self.consumer = KafkaConsumer( self.topic, bootstrap_servers=[bootstrap_servers],
            auto_offset_reset='latest',
            enable_auto_commit=True,
            auto_commit_interval_ms =  5000,
            fetch_max_bytes = 128,
            max_poll_records = 100,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    def run(self):
        self.is_stopped = False
        print('Kafka Consumming on topic: ', self.topic)

        for message in self.consumer:
            if self.is_stopped:
                break
            tweets = json.loads(json.dumps(message.value))
            
            v, s = self.flair_pred(tweets['text'])
            data = { '_id': tweets['id'],
                'topic': self.topic, 'value': v,
                'timestamp': int(tweets['timestamp_ms'][:-3]),
            }   

            requests.post(self.url, json=data)

            print(data)

    def stop(self):
        self.is_stopped = True

topics = [r[:-1] for r in open('topics.txt', 'rt').readlines()]

topic = topics[0]

for topic in topics:
    # print(f"Starting consumer on topic: `{topic}`")

    ConsumerThread(topic, flair_prediction).start()