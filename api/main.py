import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from backend.npa_project.show import show_command
from backend.npa_project.config import *

topo = Devices(testBed_loc="../backend/npa_project/tb.yaml")

app = FastAPI()

# # # # # # # # # #
# TEST API

@app.get("/")
async def root():
    return {"message": "Hello World"}

# # # # # # # # # #
# Show

@app.get("/show_ip")
def show_ip(data: dict):
    try:
        res = show_command(data["device"], "show ip interface brief")
    except:
        res = {"message": "not available"}
    return res

@app.get("/show_run")
def show_run():
    try:
        res = {"message": "show running config"} # NOT DONE
    except:
        res = {"message": "not available"}
    return res

@app.get("/show_ip_route")
def show_ip_route(data: dict):
    try:
        res = show_command(data["device"], "show ip route")
    except:
        res = {"message": "not available"}
    return res

@app.get("/show_ospf")
def show_ospf(data: dict):
    try:
        res = show_command(data["device"], "show ip ospf")
    except:
        res = {"message": "not available"}
    return res

@app.get("/show_all")
def show_all(data: dict):
    try:
        res = topo.devices[data["device"]].get_device_info()
    except:
        res = {"message": "not available"}
    return res

# # # # # # # # # #
# Interface

@app.get("/ip_addr")
def get_ip(data: dict):
    try:
        res = show_command(data["device"], f"show ip interface brief {data['interface']}")
    except:
        res = {"message": "not available"}
    return res

class InterfaceIP(BaseModel):
    device: str
    interface: str
    description: str | None = None
    ip: str
    subnet: str | None = None
    status: bool

@app.post("/interface")
async def set_interface(data: InterfaceIP):
    data = data.dict()
    if not data["ip"].isalpa():
        topo.devices[data["device"]].config_interface_s(f"int {data['interface']}", "", data["ip"], data["subnet"], data["description"], data["status"])
    elif data["ip"].lower() == "dhcp":
        topo.devices[data["device"]].config_interface_d(f"int {data['interface']}", "", data["status"])
    else:
        return {"message": message}
    try:
        # temp
        show_command(data["device"], f"show ip interface brief {data['interface']}")
        message = "success"
    except:
        message = "failed"
    return {"message": message}

# # # # # # # # # #
# Routing

class OSPF(BaseModel):
    network: str
    wildcard: str
    area: int

class OSPFNetwork(BaseModel):
    device: str
    ospf: List[OSPF]

@app.post("/ospf/{process}")
def set_network_ospf(process, data: OSPFNetwork):
    data = data.dict()
    for i in data["ospf"]:
        topo.devices[data["device"]].config_ospf_add(process, i["network"], i["wildcard"], i["area"])
    return {"message": "success"}

@app.post("/ospf_del/{process}")
def del_network_ospf(process, data: OSPFNetwork):
    data = data.dict()
    for i in data["ospf"]:
        topo.devices[data["device"]].config_ospf_del(process, i["network"], i["wildcard"], i["area"])
    return {"message": "success"}

class StaticRoute(BaseModel):
    network: str
    subnet: str
    next_hop_ip: str

class StaticRouteList(BaseModel):
    device: str
    routes: List[StaticRoute]

@app.post("/route")
def set_static_route(routes: StaticRouteList):
    data = routes.routes
    for i in data:
        i = i.dict()
        topo.devices[routes.device].config_static_route_add(i["network"], i["subnet"], i["next_hop_ip"])
    return {"message": "success"}

@app.post("/route_del")
def set_static_route_del(routes: StaticRouteList):
    data = routes.routes
    for i in data:
        i = i.dict()
        topo.devices[routes.device].config_static_route_del(i["network"], i["subnet"], i["next_hop_ip"])
    return {"message": "success"}

# # # # # # # # # #
# Device

# @app.post("/hostname")
# def set_host(name):
#     return {"hostname": name}

# @app.post("/dhcp_pool")
# def set_dhcp():
#     return {"dhcp": "set dhcp pool"}

# ''' https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4000/8-2glx/configuration/guide/ntp.html '''
# @app.post("/ntp/client")
# def set_ntp_client(ntp_ip):
#     return {"ntp_server": ntp_ip}

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
