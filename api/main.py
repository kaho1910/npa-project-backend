from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# # # # # # # # # #
# TEST API

@app.get("/")
async def root():
    return {"message": "Hello World"}

# # # # # # # # # #
# Show

@app.get("/show_ip")
def show_ip():
    return {"message": "show ip int br"}

@app.get("/show_run")
def show_run():
    return {"message": "show running config"}

@app.get("/show_ip_route")
def show_ip_route():
    return {"message": "show ip route"}

@app.get("/show_ospf")
def show_ospf():
    return {"message": "show ospf"}

# # # # # # # # # #
# Interface

@app.get("/ip_addr")
def get_ip():
    return {
        "int": "Fa0/0",
        "description": "TEST TEST",
        "ip": "255.255.255.255",
        "subnet": "255.255.255.255"
        }

class InterfaceIP(BaseModel):
    interface: str
    description: str | None = None
    ip: str
    subnet: str

@app.post("/interface")
async def set_interface(data: InterfaceIP):
    data = data.dict()
    return data

class Interface(BaseModel):
    interface: str

@app.post("/interface_shut/")
def interface_shut(interface: Interface):
    interface = interface.dict()
    return {"message": f"shutdown {interface['interface']}"}

@app.post("/interface_noshut/")
def interface_noshut(interface: Interface):
    interface = interface.dict()
    return {"message": f"no shutdown {interface['interface']}"}

# # # # # # # # # #
# Routing

class OSPF(BaseModel):
    network: str
    wildcard: str
    area: int

class OSPFNetwork(BaseModel):
    ospf: List[OSPF]

@app.post("/ospf/{process}")
def set_network_ospf(process, network: OSPFNetwork):
    return {
        "ospf_process": process,
        "network": network.ospf
        }

@app.get("/route")
def get_route():
    return {"route": "This is ROUTE"}

class StaticRoute(BaseModel):
    network: str
    subnet: str
    next_hop_ip: str

class StaticRouteList(BaseModel):
    routes: List[StaticRoute]

@app.post("/route")
def set_static_route(routes: StaticRouteList):
    return {"all_routes": routes.routes}

# # # # # # # # # #
# Router

@app.post("/hostname")
def set_host(name):
    return {"hostname": name}

@app.post("/dhcp_pool")
def set_dhcp():
    return {"dhcp": "set dhcp pool"}

''' https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4000/8-2glx/configuration/guide/ntp.html '''
@app.post("/ntp/client")
def set_ntp_client(ntp_ip):
    return {"ntp_server": ntp_ip}

# # # # # # # # # #
# Telnet / SSH

@app.post("/telnet_cred")
def set_tel_cred(username, password):
    return {"telnet_cred": {
        "username": username,
        "password": password
    }}

@app.post("/ssh_cred")
def set_ssh_cred(username, password):
    return {"ssh_cred": {
        "username": username,
        "password": password
    }}
