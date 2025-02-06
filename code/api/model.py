from pydantic import BaseModel, Field
from uuid import UUID, uuid4 
from typing import Optional 

class PacketBase(BaseModel):
    srcip: Optional[str] = None
    sport: Optional[int] = None
    dstip: Optional[str] = None
    dsport: Optional[int] = None
    proto: Optional[str] = None 
    state: Optional[str] = None 
    dur: Optional[str] = None
    sbytes: Optional[int] = None
    dbytes: Optional[int] = None
    sttl: Optional[int] = None              
    dttl: Optional[int] = None 
    sloss: Optional[int] = None 
    dloss: Optional[int] = None
    service: Optional[str] = None
    sload: Optional[str] = None
    dload: Optional[str] = None
    spkts: Optional[int] = None            
    dpkts: Optional[int] = None
    swin: Optional[int] = None
    dwin: Optional[int] = None
    stcpb: Optional[int] = None            
    dtcpb: Optional[int] = None
    smeansz: Optional[int] = None
    dmeansz: Optional[int] = None
    trans_depth: Optional[int] = None 
    res_bdy_len: Optional[int] = None          
    sjit: Optional[str] = None 
    djit: Optional[str] = None 
    stime: Optional[int] = None
    ltime: Optional[int] = None
    sintpkt: Optional[str] = None      
    dintpkt: Optional[str] = None
    tcprtt: Optional[str] = None
    synack: Optional[str] = None 
    ackdat: Optional[str] = None           
    is_sm_ips_ports: Optional[bool] = None
    ct_state_ttl: Optional[int] = None
    ct_flw_http_mthd: Optional[int] = None
    is_ftp_login: Optional[bool] = None            
    ct_ftp_cmd: Optional[int] = None
    ct_srv_src: Optional[int] = None
    ct_srv_dst: Optional[int] = None
    ct_dst_ltm: Optional[int] = None
    ct_src_ltm: Optional[int] = None
    ct_src_dport_ltm: Optional[int] = None 
    ct_dst_sport_ltm: Optional[int] = None
    ct_dst_src_ltm: Optional[int] = None
    attack_cat: Optional[str] = None
    label: Optional[bool] = None

class PacketIn(PacketBase): 
    pass

class Packet(PacketBase):
    id: UUID = Field(default_factory=uuid4)

    class Config: 
        from_attributes = True