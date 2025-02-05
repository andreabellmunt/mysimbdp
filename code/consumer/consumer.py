# Based on https://github.com/rdsea/bigdataplatforms/blob/master/tutorials/basickafka/code/simple_kafka_consumer.py 

from confluent_kafka import Consumer 
import json 

if __name__ == '__main__':
    broker = 'kafka0:19092'
    group_id = "net_consumer_group"
    topic = "network_packet"

    conf = {
        'bootstrap.servers': broker, 
        'group.id': group_id
        }

    c = Consumer(**conf)
    c.subscribe([topic])

    def process_msg(sample):
        print(f"Received message: {sample}")

    try: 
        while True: # wait for data
            message = c.poll(1)
            if message is None: 
                continue
            if message.error():
                print(f"Consumer error: {message.error()}")
                continue
            json_msg = json.loads(message.value().decode("utf-8"))
            process_msg(json_msg)
    except KeyboardInterrupt:
        print("Consumer interrupted")
    finally:
        c.close()