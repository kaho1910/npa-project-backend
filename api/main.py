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
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from backend.npa_project.show import show_command
from backend.npa_project.config import *

topo = Devices(testBed_loc="../backend/npa_project/tb.yaml")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # # # # # # # # #
# TEST API

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/devices")
def get_devices():
    try:
        res = topo.get_devices()
    except:
        res = {"message": "not availabe"}
    return res

# # # # # # # # # # # # # # # # # # # #
# DEVICES

@app.post("/add_device")
def device_add(data: dict):
    try:
        topo.add_device(data["type_device"], data["hostname"], data["ip"])
    except:
        return {"message": "fail"}
    return {"message": "success"}

@app.post("/del_device")
def device_del(data: dict):
    try:
        topo.remove_device(data["hostname"])
    except:
        return {"message": "fail"}
    return {"message": "success"}

@app.post("/save")
def save(data: dict):
    try:
        topo.devices[data["device"]].save_config()
    except:
        return {"message": "fail"}
    return {"message": "success"}

# # # # # # # # # # # # # # # # # # # #
# ROUTER

# # # # # # # # # #
# Show

@app.post("/show_ip")
def show_ip(data: dict):
    try:
        res = show_command(data["device"], "show ip interface brief")
    except:
        res = {"message": "not available"}
    return res

@app.get("/show_run")
def show_run(data: dict):
    try:
        config = topo.devices[data["device"]].get_backup_config()
        res = {"message": config}
    except:
        res = {"message": "not available"}
    return res

@app.post("/show_ip_route")
def show_ip_route(data: dict):
    try:
        res = show_command(data["device"], "show ip route")
    except:
        res = {"message": "not available"}
    return res

@app.post("/show_ip_route_static")
def show_ip_route(data: dict):
    try:
        res = show_command(data["device"], "show ip route static")
    except:
        res = {"message": "not available"}
    return res

@app.post("/show_ospf")
def show_ospf(data: dict):
    try:
        res = show_command(data["device"], "show ip ospf")
    except:
        res = {"message": "not available"}
    return res

@app.post("/show_acl")
def show_acl(data: dict):
    try:
        res = show_command(data["device"], "show ip access-lists")
    except:
        res = {"message": "not available"}
    return res

@app.post("/show_all")
def show_all(data: dict):
    try:
        res = topo.devices[data["device"]].get_device_info()
    except:
        res = {"message": "not available"}
    return res

# # # # # # # # # #
# Interface

@app.post("/ip_addr")
def get_ip(data: dict):
    try:
        res = show_command(data["device"], f"show ip interface brief {data['interfaceName']}")
    except:
        res = {"message": "not available"}
    return res

class InterfaceIP(BaseModel):
    device: str
    interfaceName: str
    description: str | None = None
    ip: str
    subnet: str | None = None
    status: bool

@app.post("/interface")
async def set_interface(data: InterfaceIP):
    data = data.dict()
    if not data["ip"].isalpha():
        topo.devices[data["device"]].config_interface_s(f"int {data['interfaceName']}", "", data["ip"], data["subnet"], data["description"], data["status"])
    elif data["ip"].lower() == "dhcp":
        topo.devices[data["device"]].config_interface_d(f"int {data['interfaceName']}", "", data["status"])
    else:
        return {"message": "fail"}
    return {"message": "success"}

# # # # # # # # # #
# Routing

class OSPF(BaseModel):
    network: str
    wildcard: str
    area: int

class OSPFNetwork(BaseModel):
    device: str
    process: int
    ospf: List[OSPF]

@app.post("/ospf")
def set_network_ospf(data: OSPFNetwork):
    data = data.dict()
    try:
        for i in data["ospf"]:
            topo.devices[data["device"]].config_ospf_add(data["process"], i["network"], i["wildcard"], i["area"])
    except:
        return {"message": "fail"}
    return {"message": "success"}

@app.post("/ospf_del")
def del_network_ospf(data: OSPFNetwork):
    data = data.dict()
    try:
        for i in data["ospf"]:
            topo.devices[data["device"]].config_ospf_del(data["process"], i["network"], i["wildcard"], i["area"])
    except:
        return {"message": "fail"}
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
    try:
        for i in data:
            i = i.dict()
            topo.devices[routes.device].config_static_route_add(i["network"], i["subnet"], i["next_hop_ip"])
    except:
        return {"message": "fail"}
    return {"message": "success"}

@app.post("/route_del")
def set_static_route_del(routes: StaticRouteList):
    data = routes.routes
    try:
        for i in data:
            i = i.dict()
            topo.devices[routes.device].config_static_route_del(i["network"], i["subnet"], i["next_hop_ip"])
    except:
        return {"message": "fail"}
    return {"message": "success"}

# # # # # # # # # #
# ACLs

class AclList(BaseModel):
    device: str
    name: str
    action: str
    protocol: str
    ip: str
    wildcard: str
    dst: str
    network: str
    eq: str | None = None
    port: str | None = None

@app.post("/acl")
def add_acl(data: AclList):
    data = data.dict()
    try:
        topo.devices[data["device"]].config_acls_add(data["name"], data["action"], data["protocol"], data["ipaddr"], data["wildcard"], data["dst"], data["network"], eq="", port="")
    except:
        return {"message": "fail"}
    return {"message": "success"}

class AclDel(BaseModel):
    device: str
    name: str
    label: str

@app.post("/acl_del")
def del_acl(data: AclDel):
    data = data.dict()
    try:
        topo.devices[data["device"]].config_acls_add(data["name"], data["lavel"])
    except:
        return {"message": "fail"}
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

# @app.post("/telnet_cred")
# def set_tel_cred(username, password):
#     return {"telnet_cred": {
#         "username": username,
#         "password": password
#     }}

# @app.post("/ssh_cred")
# def set_ssh_cred(username, password):
#     return {"ssh_cred": {
#         "username": username,
#         "password": password
#     }}

# # # # # # # # # # # # # # # # # # # #
# Switch

# # # # # # # # # #
# Show

@app.post("/show_vlan")
def show_vlan(data: dict):
    try:
        res = show_command(data["device"], "show vlan")
    except:
        res = {"message": "not available"}
    return res

@app.post("/show_swp")
def show_swp(data: dict):
    try:
        res = show_command(data["device"], "show interfaces switchport")
    except:
        res = {"message": "not available"}
    return res

@app.post("/show_stp")
def show_stp(data: dict):
    try:
        res = show_command(data["device"], "show spanning-tree")
    except:
        res = {"message": "not available"}
    return res

# # # # # # # # # #
# Vlan

class Vlan(BaseModel):
    device: str
    vlan: int
    name: str
    ip: str
    subnet: str
    description: str | None = None
    status: bool

@app.post("/vlan")
def add_vlan(data: Vlan):
    data = data.dict()
    try:
        topo.devices[data["device"]].config_vlan_add(f"vlan {data['vlan']}", data["name"], data["ip"], data["subnet"], data["description"], data["status"])
    except:
        return {"message": "fail"}
    return {"message": "success"}

@app.post("/vlan_del")
def del_vlan(data: dict):
    try:
        topo.devices[data.device].config_vlan_del(data.vlan)
    except:
        return {"message": "fail"}
    return {"message": "success"}

class VlanMode(BaseModel):
    device: str
    interfaceName: str
    vlan: int
    allow: str | None = None
    status: bool

@app.post("/vlan_access")
def config_vlan_a(data: VlanMode):
    data = data.dict()
    try:
        topo.devices[data["device"]].config_interface_sw_a(data["interfaceName"], data["vlan"], data["status"])
    except:
        return {"message": "fail"}
    return {"message": "success"}

@app.post("/vlan_trunk")
def config_vlan_t(data: VlanMode):
    data = data.dict()
    try:
        topo.devices[data["device"]].config_interface_sw_a(data["interfaceName"], data["vlan"], data["allow"], data["status"])
    except:
        return {"message": "fail"}
    return {"message": "success"}
