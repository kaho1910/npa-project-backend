from pyats.topology import loader

class Interface:
    """"""
    def __init__(self, mode: str, ipaddr: str, subnet: str, status: bool) -> None:
        self.mode = mode
        self.ipaddr = ipaddr
        self.subnet = subnet
        self.status = status

class Routes:
    """"""
    def __init__(self, info: dict) -> None:
        self.info = info
        self.load_data()

    def load_data(self) -> None:
        print(self.info)

class OSPF:
    """"""
    def __init__(self, info: dict) -> None:
        self.info = info
        self.load_data()

    def load_data(self) -> None:
        print(self.info)

class ACLS:
    """"""
    def __init__(self, info: dict) -> None:
        self.info = info
        self.load_data()

    def load_data(self) -> None:
        print(self.info)

class Device:
    """""""" 
    import abc

    @abc.abstractmethod
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

    def config_interface_d(self, interface: str, mode: str, status: bool) -> None:
        # self.interfaces[interface].mode = mode
        # self.interfaces[interface].status = status
        config = """
        {}
            ip add dhcp
            {}
        """
        self.testbed.configure(config.format(interface, "no shut" if status else "shut"))
    
    def config_interface_s(self, interface: str, mode: str, ipaddr: str, subnet: str, status: bool) -> None:
        # self.interfaces[interface].mode = mode
        # self.interfaces[interface].ipaddr = ipaddr
        # self.interfaces[interface].subnet = subnet
        # self.interfaces[interface].status = status
        config = config = """
        {}
            ip add {} {}
            {}
        """
        self.testbed.configure(config.format(interface, ipaddr, subnet, "no shut" if status else "shut"))
    
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

    def config_ospf_add(self, network: str, wildcard: str, area: int) -> None:
        config = """
        router ospf 1
            network {} {} area {}
        """
        self.testbed.configure(config.format(network, wildcard, area))
    
    def config_ospf_del(self, network: str, wildcard: str, area: int) -> None:
        config = """
        router ospf 1
            no network {} {} area {}
        """
        self.testbed.configure(config.format(network, wildcard, area))

    def config_acls_add1(self, name: str, action: str, protocol: str, eq="", port="") -> None:
        config = """
        ip access-list extended {}
            {} {} any any {} {}
        """
        self.testbed.configure(config.format(name, action, protocol, eq, port))
    
    def config_acls_add2(self, name: str, action: str, protocol: str, ipaddr: str, wildcard: str, eq="", port="") -> None:
        config = """
        ip access-list extended {}
            {} {} {} {} any {} {}
        """
        self.testbed.configure(config.format(name, action, protocol, ipaddr, wildcard, eq, port))

    def config_acls_add3(self, name: str, action: str, protocol: str, ipaddr: str, wildcard: str, dst: str, network: str, eq="", port="") -> None:
        config = """
        ip access-list extended {}
            {} {} {} {} {} {} {} {}
        """
        self.testbed.configure(config.format(name, action, protocol, ipaddr, wildcard, dst, network, eq, port))
    
    def config_acls_add4(self, name: str, action: str, protocol: str, dst: str, network: str, eq="", port="") -> None:
        config = """
        ip access-list extended {}
            {} {} any {} {} {} {}
        """
        self.testbed.configure(config.format(name, action, protocol, dst, network, eq, port))

    def config_acls_del(self, name: str, label: int) -> None:
        config = """
        ip access-list extended {}
            no {}
        """
        self.testbed.configure(config.format(name, label))

    def get_backup_config(self) -> str:
        self.testbed.connect()
        return self.testbed.execute("show run")
    
    def add_backup_config(self, config: str) -> None:
        self.testbed.connect()
        self.testbed.config(config)

    def save_config(self):
        self.testbed.connect()
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
        print(self.info)

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
        self.testbed.connect()
        print(type(self.get_device_info()))
        self.interfaces = R_Interfaces(self.int_load)
        self.static_routes = Routes(self.route_load)
        self.ospf = OSPF(self.ospf_load)
        self.acls = ACLS(self.acls_load)

class SW_Device(Device):
    """"""
    def __init__(self, testbed) -> None:
        self.testbed = testbed
        self.load_data()

    def load_data(self) -> None:
        self.testbed.connect()
        print(type(self.get_device_info()))
        self.interfaces = SW_Interfaces(self.int_load)
        self.static_routes = Routes(self.route_load)
        self.ospf = OSPF(self.ospf_load)
        self.acls = ACLS(self.acls_load)

    def get_device_info(self) -> dict:
        try:
            self.int_load = self.testbed.parse("show ip interface brief")
        except:
            print("Error parsing")
        try:
            self.vlan_load = self.testbed.parse("show vlan")
        except:
            print("Error parsing")
        try:
            self.stp_load = self.testbed.parse("show spanning-tree")
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
            "vlan": self.vlan_load,
            "stp": self.stp_load,
            "routes": self.route_load,
            "ospf": self.ospf_load,
            "acls": self.acls_load
        }
    
    def device_test_connection(self) -> bool:
        try:
            self.testbed.connect()
            return True
        except:
            return False
    def config_interface_d(self, interface: str, mode: str, status: bool) -> None:
        config = """
        {}
            no sw
            ip add dhcp
            {}
        """
        self.testbed.configure(config.format(interface, "no shut" if status else "shut"))
    
    def config_interface_s(self, interface: str, mode: str, ipaddr: str, subnet: str, status: bool) -> None:
        config = config = """
        {}
            no sw
            ip add {} {}
            {}
        """
        self.testbed.configure(config.format(interface, ipaddr, subnet, "no shut" if status else "shut"))
    
    def config_interface_sw_a(self, interface: str, vlan: int, status: bool) -> None:
        config = config = """
        {}
            switchport mode access
            switchport access vlan {}
            {}
        """
        self.testbed.configure(config.format(interface, vlan, "no shut" if status else "shut"))
    
    def config_interface_sw_t(self, interface: str, vlan: int, allow: str, status: bool) -> None:
        config = config = """
        {}
            switchport mode trunk
            switchport trunk native vlan {}
            switchport trunk allowed vlan {}
            {}
        """
        self.testbed.configure(config.format(interface, vlan, allow, "no shut" if status else "shut"))

    def config_vlan_add(self, interface: str, name: str, ipaddr: str, subnet: str, status: bool) -> None:
        config = config = """
        {}
            name {}
        int {}
            ip add {}
            {}
        """
        self.testbed.configure(config.format(interface, name, ipaddr, subnet, "no shut" if status else "shut"))

    def config_vlan_del(self, interface: str) -> None:
        config = config = """
        no int {}
        no {}
        """
        self.testbed.configure(config.format(interface, interface))

class Devices:
    """"""
    def __init__(self) -> None:
        self.devices = {}
        self.testbed = loader.load('my_testbed.yaml')
        for x in self.testbed.devices:
            device = self.testbed.devices[x]
            if device.custom.type == "Router":
                self.add_devices(R_Device(device))
            else:
                self.add_devices(SW_Device(device))
        print(self.get_devices())

    def add_devices(self, device: Device) -> None:
        self.devices[device.testbed.custom.hostname] = device
        print(device.testbed.custom.hostname)

    def add_device(self, type: str, hostname: str, ipaddr: str) -> None:
        # add device to yaml file

        if type == "Router":
            device = R_Device(loader.load('my_testbed.yaml').devices['hostname'])
        else:
            device = SW_Device(loader.load('my_testbed.yaml').devices['hostname'])
        self.devices[hostname] = device

    def remove_device(self, hostname: str) -> None:
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
    json.dump(topo.devices["test"].get_device_info(), open('test-topo.json', 'w'), indent=2)
