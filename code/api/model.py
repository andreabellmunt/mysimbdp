from pydantic import BaseModel, Field
from uuid import UUID, uuid4 
from typing import Optional 


class PacketBase(BaseModel):
    srcip: Optional[str] = None
    sport: Optional[str] = None
    dstip: Optional[str] = None
    dsport: Optional[str] = None
    proto: Optional[str] = None 
    state: Optional[str] = None 
    dur: Optional[str] = None
    sbytes: Optional[str] = None
    dbytes: Optional[str] = None
    sttl: Optional[str] = None              
    dttl: Optional[str] = None 
    sloss: Optional[str] = None 
    dloss: Optional[str] = None
    service: Optional[str] = None
    sload: Optional[str] = None
    dload: Optional[str] = None
    spkts: Optional[str] = None            
    dpkts: Optional[str] = None
    swin: Optional[str] = None
    dwin: Optional[str] = None
    stcpb: Optional[str] = None            
    dtcpb: Optional[str] = None
    smeansz: Optional[str] = None
    dmeansz: Optional[str] = None
    trans_depth: Optional[str] = None 
    res_bdy_len: Optional[str] = None          
    sjit: Optional[str] = None 
    djit: Optional[str] = None 
    stime: Optional[str] = None
    ltime: Optional[str] = None
    sintpkt: Optional[str] = None      
    dintpkt: Optional[str] = None
    tcprtt: Optional[str] = None
    synack: Optional[str] = None 
    ackdat: Optional[str] = None           
    is_sm_ips_ports: Optional[str] = None
    ct_state_ttl: Optional[str] = None
    ct_flw_http_mthd: Optional[str] = None
    is_ftp_login: Optional[str] = None            
    ct_ftp_cmd: Optional[str] = None
    ct_srv_src: Optional[str] = None
    ct_srv_dst: Optional[str] = None
    ct_dst_ltm: Optional[str] = None
    ct_src_ltm: Optional[str] = None
    ct_src_dport_ltm: Optional[str] = None 
    ct_dst_sport_ltm: Optional[str] = None
    ct_dst_src_ltm: Optional[str] = None
    attack_cat: Optional[str] = None
    label: Optional[str] = None

class PacketIn(PacketBase): 
    pass

class Packet(PacketBase):
    id: UUID = Field(default_factory=uuid4)

    class Config: 
        from_attributes = True