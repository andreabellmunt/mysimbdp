# Based on https://dev.to/csar_fabinchvezlinar/building-a-task-management-api-with-apache-cassandra-and-fastapi-3ho0

from cassandra.cluster import Cluster


class CassandraConnection:
    def __init__(self): 
        self.cluster = None
        self.session = None
    async def connect(self, host=['cassandra0', 'cassandra1', 'cassandra2']): 
        self.cluster = Cluster(host)
        self.session = self.cluster.connect()

        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS packet_manager
            WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3}
        """)

        self.session.set_keyspace('packet_manager')

        self.session.execute("""
            CREATE TABLE IF NOT EXISTS packets (
                id uuid,
                srcip text,
                sport int,
                dstip text,
                dsport int,
                proto text, 
                state text, 
                dur text,
                sbytes int,
                dbytes int,
                sttl int,              
                dttl int, 
                sloss int, 
                dloss int, 
                service text,
                sload text, 
                dload text, 
                spkts int,             
                dpkts int, 
                swin int, 
                dwin int, 
                stcpb int,            
                dtcpb int,
                smeansz int, 
                dmeansz int, 
                trans_depth int, 
                res_bdy_len int,           
                sjit text, 
                djit text, 
                stime int, 
                ltime int, 
                sintpkt text,        
                dintpkt text,
                tcprtt text,
                synack text, 
                ackdat text,           
                is_sm_ips_ports boolean,
                ct_state_ttl int, 
                ct_flw_http_mthd int, 
                is_ftp_login boolean,             
                ct_ftp_cmd int, 
                ct_srv_src int,
                ct_srv_dst int, 
                ct_dst_ltm int,
                ct_src_ltm int, 
                ct_src_dport_ltm int, 
                ct_dst_sport_ltm int,
                ct_dst_src_ltm int,
                attack_cat text, 
                label boolean,
                PRIMARY KEY (id)
            )
        """) # stime and ltime are supposedly timestamps but process as int based on data source 
        # all decimal values passed to text because of issues with decimal 

        return self.session
    
    async def disconnect(self):
        if self.cluster:
            self.cluster.shutdown()

db = CassandraConnection()

async def get_db():
    try:
        session = await db.connect()
        yield session
    finally:
        await db.disconnect()
