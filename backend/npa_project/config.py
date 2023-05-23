from pyats.topology import loader

class Interface:
    """"""
    def __init__(self, info: dict) -> None:
        self.info = info
        self.load_data()

    def load_data(self) -> None:
        # print(self.info)
        pass

class Routes:
    """"""
    def __init__(self, info: dict) -> None:
        self.info = info
        self.load_data()

    def load_data(self) -> None:
        pass

class OSPF:
    """"""
    def __init__(self, info: dict) -> None:
        self.info = info
        self.load_data()

    def load_data(self) -> None:
        pass

class ACLS:
    """"""
    def __init__(self, info: dict) -> None:
        self.info = info
        self.load_data()

    def load_data(self) -> None:
        pass

class Device:
    """"""""
    def device_test_connection(self) -> bool:
        try:
            self.testbed.connect()
            return True
        except:
            return False

    def get_device_info(self) -> dict:
        try:
            self.int_load = self.testbed.parse("show ip interface brief")
        except:
            print("Error parsing")
        try:
            self.route_load = self.testbed.parse("show ip static route")
        except:
            print("Error parsing")
        try:
            self.ospf_load = self.testbed.parse("show ip ospf")
        except:
            print("Error parsing")
        try:
            self.acls_load = self.testbed.parse("show ip access-lists")
        except:
            print("Error parsing")
        return {
            "interfaces": self.int_load,
            "routes": self.route_load,
            "ospf": self.ospf_load,
            "acls": self.acls_load
        }

    def config_interface_d(self, interface: str, mode: str, desc: str,status: bool) -> None:
        # self.interfaces[interface].mode = mode
        # self.interfaces[interface].status = status
        if desc is None:
            desc = "\n"
        else:
            desc = "desc " + desc
        config = """
        {}
            ip add dhcp
            {}
            {}
        """
        self.testbed.configure(config.format(interface, desc, "no shut" if status else "shut"))
    
    def config_interface_s(self, interface: str, mode: str, ipaddr: str, subnet: str, desc: str, status: bool) -> None:
        # self.interfaces[interface].mode = mode
        # self.interfaces[interface].ipaddr = ipaddr
        # self.interfaces[interface].subnet = subnet
        # self.interfaces[interface].status = status
        if desc is None:
            desc = "\n"
        else:
            desc = "desc " + desc
        config = """
        {}
            ip add {} {}
            {}
            {}
        """
        self.testbed.configure(config.format(interface, ipaddr, subnet, desc,"no shut" if status else "shut"))
    
    def config_static_route_add(self, dst: str, network: str, next_hop: str) -> None:
        config = """
        ip route {} {} {}
        """
        self.testbed.configure(config.format(dst, network, next_hop))
    
    def config_static_route_del(self, dst: str, network: str, next_hop: str) -> None:
        config = """
        no ip route {} {} {}
        """
        self.testbed.configure(config.format(dst, network, next_hop))

    def config_ospf_add(self, process: int, network: str, wildcard: str, area: int) -> None:
        config = """
        router ospf {}
            network {} {} area {}
        """
        self.testbed.configure(config.format(process, network, wildcard, area))
    
    def config_ospf_del(self, process: int, network: str, wildcard: str, area: int) -> None:
        config = """
        router ospf {}
            no network {} {} area {}
        """
        self.testbed.configure(config.format(process, network, wildcard, area))

    def config_acls_add(self, name: str, action: str, protocol: str, ipaddr: str, wildcard: str, dst: str, network: str, eq="", port="") -> None:
        config = """
        ip access-list extended {}
            {} {} {} {} {} {} {} {}
        """
        self.testbed.configure(config.format(name, action, protocol, ipaddr, wildcard, dst, network, eq, port))

    def config_acls_del(self, name: str, label: int) -> None:
        config = """
        ip access-list extended {}
            no {}
        """
        self.testbed.configure(config.format(name, label))

    def get_backup_config(self) -> str:
        self.testbed.connect(log_stdout=False)
        return self.testbed.execute("show run")
    
    def add_backup_config(self, config: str) -> None:
        self.testbed.connect(log_stdout=False)
        self.testbed.config(config)

    def save_config(self):
        self.testbed.connect(log_stdout=False)
        self.testbed.execute("write")

class SW_Interface(Interface):
    """"""
    def set_switchport(self, sw: bool) -> str:
        return "Now Switchport is " + ("en" if sw else "dis") + "able."

class R_Interfaces:
    """"""
    def __init__(self, info: dict) -> None:
        self.info = info
        self.load_data()

    def load_data(self) -> None:
        # print(self.info)
        pass

    # def add_interface(self, interface: Interface) -> None:
    #     self.interfaces.append(interface)

class SW_Interfaces:
    """"""
    def __init__(self, info: dict) -> None:
        self.info = info
        self.load_data()

    def load_data(self) -> None:
        print(self.info)

    # def add_interface(self, interface: Interface) -> None:
    #     self.interfaces.append(interface)

class R_Device(Device):
    """"""
    def __init__(self, testbed) -> None:
        self.testbed = testbed
        self.load_data()

    def load_data(self) -> None:
        self.testbed.connect(log_stdout=False)
        self.interfaces = R_Interfaces(self.int_load)
        self.static_routes = Routes(self.route_load)
        self.ospf = OSPF(self.ospf_load)
        self.acls = ACLS(self.acls_load)

    def get_device_info(self) -> dict:
        try:
            self.int_load = self.testbed.parse("show ip interface brief")
        except:
            self.int_load = {}
            print("ParseError")
        try:
            self.route_load = self.testbed.parse("show ip static route")
        except:
            self.route_load = {}
            print("ParseError")
        try:
            self.ospf_load = self.testbed.parse("show ip ospf")
        except:
            self.ospf_load = {}
            print("ParseError")
        try:
            self.acls_load = self.testbed.parse("show ip access-lists")
        except:
            self.acls_load = {}
            print("ParseError")
        return {
            "interfaces": self.int_load,
            "routes": self.route_load,
            "ospf": self.ospf_load,
            "acls": self.acls_load
        }

class SW_Device(Device):
    """"""
    def __init__(self, testbed) -> None:
        self.testbed = testbed
        self.load_data()

    def load_data(self) -> None:
        self.testbed.connect(log_stdout=False)
        self.get_device_info()
        self.interfaces = SW_Interfaces(self.int_load)
        self.static_routes = Routes(self.route_load)
        self.ospf = OSPF(self.ospf_load)
        self.acls = ACLS(self.acls_load)

    def get_device_info(self) -> dict:
        try:
            self.int_load = self.testbed.parse("show ip interface brief")
        except:
            self.int_load = {}
            print("Error parsing")
        try:
            self.vlan_load = self.testbed.parse("show vlan")
        except:
            self.vlan_load = {}
            print("Error parsing")
        try:
            self.stp_load = self.testbed.parse("show spanning-tree")
        except:
            self.stp_load = {}
            print("Error parsing")
        try:
            self.route_load = self.testbed.parse("show ip static route")
        except:
            self.route_load = {}
            print("Error parsing")
        try:
            self.ospf_load = self.testbed.parse("show ip ospf")
        except:
            self.ospf_load = {}
            print("Error parsing")
        try:
            self.switchport_load = self.testbed.parse("show interfaces switchport")
        except:
            self.switchport_load = {}
            print("Error parsing")
        try:
            self.acls_load = self.testbed.parse("show ip access-lists")
        except:
            self.acls_load = {}
            print("Error parsing")
        return {
            "interfaces": self.int_load,
            "vlan": self.vlan_load,
            "stp": self.stp_load,
            "routes": self.route_load,
            "ospf": self.ospf_load,
            "switchport": self.switchport_load,
            "acls": self.acls_load
        }

    def config_interface_d(self, interface: str, mode: str, desc: str, status: bool) -> None:
        config = """
        {}
            no sw
            ip add dhcp
            {}
            {}
        """
        self.testbed.configure(config.format(interface, desc, "no shut" if status else "shut"))
    
    def config_interface_s(self, interface: str, mode: str, ipaddr: str, subnet: str, desc: str, status: bool) -> None:
        if desc is None:
            desc = "\n"
        else:
            desc = "desc " + desc
        config = """
        {}
            no sw
            ip add {} {}
            {}
            {}
        """
        self.testbed.configure(config.format(interface, ipaddr, subnet, desc, "no shut" if status else "shut"))
    
    def config_interface_sw_a(self, interface: str, vlan: int, status: bool) -> None:
        config = """
        {}
            switchport mode access
            switchport access vlan {}
            {}
        """
        self.testbed.configure(config.format(interface, vlan, "no shut" if status else "shut"))
    
    def config_interface_sw_t(self, interface: str, vlan: int, allow: str, status: bool) -> None:
        config = """
        {}
            switchport mode trunk
            switchport trunk native vlan {}
            switchport trunk allowed vlan {}
            {}
        """
        self.testbed.configure(config.format(interface, vlan, allow, "no shut" if status else "shut"))

    def config_vlan_add(self, vlan: str, name: str, ipaddr: str, subnet: str, desc: str, status: bool) -> None:
        if desc is None:
            desc = "\n"
        else:
            desc = "desc " + desc
        config = """
        vlan {}
            name {}
        int vlan {}
            ip add {} {}
            {}
            {}
        """
        self.testbed.configure(config.format(vlan, name, vlan, ipaddr, subnet, desc, "no shut" if status else "shut"))

    def config_vlan_del(self, vlan: str) -> None:
        config = """
        no int vlan {}
        no vlan {}
        """
        self.testbed.configure(config.format(vlan, vlan))

class Devices:
    """"""
    def __init__(self, testBed_loc="my_testbed.yaml") -> None:
        self.devices = {}
        self.testbed_loc = testBed_loc
        self.testbed = loader.load(self.testbed_loc)
        for x in self.testbed.devices:
            device = self.testbed.devices[x]
            if device.custom.type == "Router":
                self.add_devices(R_Device(device))
            else:
                self.add_devices(SW_Device(device))
                pass
        # print(self.get_devices())

    def add_devices(self, device: Device) -> None:
        self.devices[device.testbed.custom.hostname] = device

    def add_device(self, type: str, hostname: str, ipaddr: str) -> None:
        # add device to yaml file

        if type == "Router":
            device = R_Device(loader.load(self.testbed_loc).devices['hostname'])
        else:
            device = SW_Device(loader.load(self.testbed_loc).devices['hostname'])
        self.devices[hostname] = device

    def remove_device(self, hostname: str) -> None:
        # remove device from yaml file
        
        del self.devices[hostname]

    def get_devices(self) -> list:
        import json

        def list_to_json(data):
            json.dump(data, open('test.json', 'w'), indent=2)

        devices = []
        for device in self.devices:
            data = self.devices[device].testbed.custom
            data["status"] = self.devices[device].device_test_connection()
            devices.append(data)
        list_to_json(devices)
        return devices

import json
if __name__ == '__main__':
    topo = Devices()
    print(topo.devices["RS"].device_test_connection())
    print(topo.devices["test"].device_test_connection())
    # json.dump(topo.devices["R1"].get_device_info(), open('test-topo.json', 'w'), indent=2)
