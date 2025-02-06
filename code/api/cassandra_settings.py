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
                sport text,
                dstip text,
                dsport text,
                proto text, 
                state text, 
                dur text,
                sbytes text,
                dbytes text,
                sttl text,              
                dttl text, 
                sloss text, 
                dloss text, 
                service text,
                sload text, 
                dload text, 
                spkts text,             
                dpkts text, 
                swin text, 
                dwin text, 
                stcpb text,            
                dtcpb text,
                smeansz text, 
                dmeansz text, 
                trans_depth text, 
                res_bdy_len text,           
                sjit text, 
                djit text, 
                stime text, 
                ltime text, 
                sintpkt text,        
                dintpkt text,
                tcprtt text,
                synack text, 
                ackdat text,           
                is_sm_ips_ports text,
                ct_state_ttl text, 
                ct_flw_http_mthd text, 
                is_ftp_login text,             
                ct_ftp_cmd text, 
                ct_srv_src text,
                ct_srv_dst text, 
                ct_dst_ltm text,
                ct_src_ltm text, 
                ct_src_dport_ltm text, 
                ct_dst_sport_ltm text,
                ct_dst_src_ltm text,
                attack_cat text, 
                label text,
                PRIMARY KEY (id)
            )
        """) 

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
