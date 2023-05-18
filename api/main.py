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
