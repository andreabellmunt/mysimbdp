# Based on https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/producer.py

from confluent_kafka import Producer
from pandas import read_csv
import sys
import json

if __name__ == '__main__':
    broker = 'kafka0:19092' # first broker connection 
    topic = "network_packet"
    csv_file = "./data/test.csv" #!!! CHANGE 

    conf = {'bootstrap.servers': broker}

    p = Producer(**conf)

    def delivery_callback(err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s [%d] @ %d\n' %
                            (msg.topic(), msg.partition(), msg.offset()))
    
    def transform_json(row): 
        columns = ['srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'service', 'sload', 'dload', 'spkts', 'dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'sjit', 'djit', 'stime', 'ltime', 'sintpkt', 'dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attack_cat', 'label'] # column names 
        row_dict = dict(zip(columns, row)) # dict with columns as key 
        for key in row_dict: # transform empty vals to null 
            if row_dict[key] == '':
                row_dict[key] = None
        return json.dumps(row_dict)
    
    with open(csv_file, mode='r') as file:
        read_file = read_csv(csv_file, sep = ",")
        for index, row in read_file.iterrows():
            try:
                message = transform_json(row)
                p.produce(topic, message, callback=delivery_callback)

            except BufferError:
                sys.stderr.write('%% Producer queue busy (%d messages waiting)\n' %
                                len(p))
            p.poll(0)

    # Until all messages delivered 
    sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
    p.flush()