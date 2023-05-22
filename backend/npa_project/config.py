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

    def set_device(self, ) -> None:
        pass

    @abc.abstractmethod
    def device_test_connection(self) -> bool:
        pass

    def get_device_info(self) -> dict:
        self.int_load = self.testbed.parse("show ip interface brief")
        self.route_load = self.testbed.parse("show ip static route")
        self.ospf_load = self.testbed.parse("show ip ospf")
        self.acls_load = self.testbed.parse("show ip access-lists")
        return {
            "interfaces": self.int_load,
            "routes": self.route_load,
            "ospf": self.ospf_load,
            "acls": self.acls_load
        }

    def config_interface_d(self, interface: str, mode: str, desc: str,status: bool) -> None:
        # self.interfaces[interface].mode = mode
        # self.interfaces[interface].status = status
        if desc == "":
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
        if desc == "":
            desc = "\n"
        else:
            desc = "desc " + desc
        config = config = """
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

    def config_acls(self, name: str, action: str, protocol: str) -> None:
        config = """
        ip access-list extended {}
            {} {} any any
        """
        self.testbed.configure(config.format(name, action, protocol))
    
    def config_acls(self, name: str, action: str, protocol: str) -> None:
        config = """
        ip access-list extended {}
            {} {} {} any
        """
        self.testbed.configure(config.format(name, action, protocol))

    def get_backup_config(self) -> str:
        self.testbed.connect(log_stdout=False)
        return self.testbed.execute("show run")
    
    def add_backup_config(self, config: str) -> None:
        self.testbed.connect(log_stdout=False)
        self.testbed.config(config)

    def save_config(self):
        self.testbed.connect(log_stdout=False)
        self.testbed.execute("write")

class R_Interfaces:
    """"""
    def __init__(self, info: dict) -> None:
        self.info = info
        self.load_data()

    def load_data(self) -> None:
        print(self.info)

    # def add_interface(self, interface: Interface) -> None:
    #     self.interfaces.append(interface)

# class SW_Interface(Interface):
    """"""
    def set_switchport(self, sw: bool) -> str:
        return "Now Switchport is " + ("en" if sw else "dis") + "able."

class R_Device(Device):
    """"""
    def __init__(self, testbed) -> None:
        self.testbed = testbed
        self.load_data()

    def load_data(self) -> None:
        self.testbed.connect(log_stdout=False)
        type(self.get_device_info())
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
    
    def device_test_connection(self) -> bool:
        try:
            self.testbed.connect(log_stdout=False)
            return True
        except:
            return False

class SW_Device(Device):
    """"""
    def __init__(self, testbed: any) -> None:
        super(testbed)

    def load_data(self) -> None:
        self.testbed.connect(log_stdout=False)
        type(self.get_device_info())
        self.interfaces = R_Interfaces(self.int_load)
        self.static_routes = Routes(self.route_load)
        self.ospf = OSPF(self.ospf_load)
        self.acls = ACLS(self.acls_load)

    def get_device_info(self) -> dict:
        self.int_load = self.testbed.parse("show ip interface brief")
        self.route_load = self.testbed.parse("show ip static route")
        self.ospf_load = self.testbed.parse("show ip ospf")
        self.acls_load = self.testbed.parse("show ip access-lists")
        return {
            "interfaces": self.int_load,
            "routes": self.route_load,
            "ospf": self.ospf_load,
            "acls": self.acls_load
        }
    
    def device_test_connection(self) -> bool:
        try:
            self.testbed.connect(log_stdout=False)
            return True
        except:
            return False

class Devices:
    """"""
    def __init__(self, testBed_loc) -> None:
        self.devices = {}
        self.testbed_loc = testBed_loc
        self.testbed = loader.load(self.testbed_loc)
        for x in self.testbed.devices:
            device = self.testbed.devices[x]
            if device.custom.type == "Router":
                self.add_devices(R_Device(device))
            else:
                # self.add_devices(SW_Device(device))
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

if __name__ == '__main__':
    topo = Devices(testBed_loc='backend/npa_project/tb.yaml')
    print(topo.devices["R1"].get_device_info())
    topo.devices["R1"].config_interface_s("int lo0", "static", "1.1.1.1", "255.255.255.255", False)
    print(repr(topo.devices["R1"].interfaces))
    # test1 = Interface("interface GigabitEthernet0/3", "static", "10.0.15.201/24", True)
    # test2 = Interface("interface GigabitEthernet0/0", "static", "172.16.1.1/24", True)
    # test3 = SW_Interface("interface GigabitEthernet0/0", "static", "172.16.1.1/24", True)
    # print(test3.set_switchport(True))
    # r1 = R_Interfaces("R1", [])
    # print(r1.interfaces)
    # print(test1.ip_add)
    # r1.add_interface(test1)
    # test1.set_ip_add("1.1.1.1/32")
    # print(test1.ip_add)
    # print(test1)
    # r1.add_interface(test1)
    # r1.add_interface(test2)
    # print(r1.interfaces[0].ip_add)
    # print(r1.interfaces[1].ip_add)
    # r1.interfaces[0].set_ip_add("2.2.2.1/32")
    # print(r1.interfaces[0].ip_add)
    # print(r1.interfaces[1].ip_add)
