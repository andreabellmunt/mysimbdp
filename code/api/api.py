from fastapi import FastAPI, Depends
from model import PacketIn
from cassandra.cluster import Session
from cassandra_settings import get_db 
import uuid 

app = FastAPI()

@app.post("/cassandra")
async def save_packet(packet: PacketIn, db: Session = Depends(get_db)):
    id = uuid.uuid4()

    query = """
        INSERT INTO packets ( id, srcip, sport, dstip,dsport,proto, state, dur, sbytes, dbytes, sttl, dttl,  sloss,  dloss,  service, sload,  dload,  spkts, dpkts,  swin,  dwin,  stcpb, dtcpb, smeansz,  dmeansz,  trans_depth,  res_bdy_len, sjit,  djit,  stime,  ltime,  sintpkt, dintpkt, tcprtt, synack,  ackdat, is_sm_ips_ports boolean,ct_state_ttl,  ct_flw_http_mthd,  is_ftp_login boolean, ct_ftp_cmd,  ct_srv_src, ct_srv_dst,  ct_dst_ltm, ct_src_ltm,  ct_src_dport_ltm,  ct_dst_sport_ltm, ct_dst_src_ltm, attack_cat,  label boolean)
        VALUES (%s, %s, %d, %s, %d, %s, %s, %d, %d, %d, %d, %d, %d, %d, %s, %s, %s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %s, %s, %d, %d, %s, %s, %s, %s, %s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %s, %d)
    """

    db.execute(query, (
        id, 
        packet.srcip,
        packet.sport,
        packet.dstip,
        packet.dsport,
        packet.proto,
        packet.state, 
        packet.dur,
        packet.sbytes,
        packet.dbytes,
        packet.sttl,              
        packet.dttl, 
        packet.sloss, 
        packet.dloss,
        packet.service,
        packet.sload,
        packet.dload,
        packet.spkts,           
        packet.dpkts,
        packet.swin,
        packet.dwin,
        packet.stcpb,            
        packet.dtcpb,
        packet.smeansz,
        packet.dmeansz,
        packet.trans_depth, 
        packet.res_bdy_len,          
        packet.sjit, 
        packet.djit, 
        packet.stime,
        packet.ltime,
        packet.sintpkt,      
        packet.dintpkt,
        packet.tcprtt,
        packet.synack, 
        packet.ackdat,           
        packet.is_sm_ips_ports,
        packet.ct_state_ttl,
        packet.ct_flw_http_mthd,
        packet.is_ftp_login,            
        packet.ct_ftp_cmd,
        packet.ct_srv_src,
        packet.ct_srv_dst,
        packet.ct_dst_ltm,
        packet.ct_src_ltm,
        packet.ct_src_dport_ltm, 
        packet.ct_dst_sport_ltm,
        packet.ct_dst_src_ltm,
        packet.attack_cat,
        packet.label
    ))

    return packet