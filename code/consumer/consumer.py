# Based on https://github.com/rdsea/bigdataplatforms/blob/master/tutorials/basickafka/code/simple_kafka_consumer.py 

from confluent_kafka import Consumer 
import requests
import json 
import math 
import time


def transform_sample(data): # pass all to null or string 
    if isinstance(data, dict):
        return {key: transform_sample(value) for key, value in data.items()}
    elif isinstance(data, float):
        if math.isnan(data):
            return None  
        return str(data)  
    elif isinstance(data, (str, int, bool)):
        if isinstance(data, str) and data.strip() in [" ", "NaN", "nan", ""]:
            return None  
        return str(data)  
    return None  


def process_msg(sample):
    # To save data to Cassandra an API is used 
    transf_sample = transform_sample(sample)
    print(transf_sample)
    try:
        response = requests.post(API_URL, json=transf_sample)
        print(f"Response: {response.status_code}, {response.json()}")
    except Exception as e:
        print(f"Error sending data to API: {e}")
        
if __name__ == '__main__':
    broker = 'kafka0:19092'
    group_id = "net_consumer_group"
    topic = "network_packet"
    API_URL = "http://api:8080/cassandra"


    conf = {
        'bootstrap.servers': broker, 
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
    }

    c = Consumer(**conf)
    c.subscribe([topic])

    try: 
        while True: # wait for data
            message = c.poll(1)
            if message is None: 
                continue
            if message.error():
                print(f"Consumer error: {message.error()}")
                continue
            json_msg = json.loads(message.value())
            process_msg(json_msg)
    except KeyboardInterrupt:
        print("Consumer interrupted")
    finally:
        c.close()