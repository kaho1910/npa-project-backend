class R_Interface:
    """"""
    def __init__(self, name: str, mode: str, ip_add: str, status: bool) -> None:
        self.name = name
        self.ip_add_mode = mode
        self.ip_add = ip_add
        self.status = status
    def set_ip_add(self, ip_add: str) -> None:
        self.ip_add = ip_add

class R_Interfaces:
    """"""
    def __init__(self, hostname: str, interface: list) -> None:
        self.hostname = hostname
        self.interfaces = interface
    def add_interface(self, interface: R_Interface) -> None:
        self.interfaces.append(interface)
        
class SW_Interface(R_Interface):
    """"""
    # def __init__(self, sw: bool) -> None:
    #     self.switchport = sw
    def set_switchport(self, sw: bool) -> str:
        return "Now Switchport is " + ("en" if sw else "dis") + "able."
    
class SW_Interfaces(R_Interfaces):
    """"""
    def set_switchport(self, sw: bool) -> str:
        return "Now Switchport is " + ("en" if sw else "dis") + "able."

if __name__ == '__main__':
    test1 = R_Interface("interface GigabitEthernet0/3", "static", "10.0.15.201/24", True)
    test2 = R_Interface("interface GigabitEthernet0/0", "static", "172.16.1.1/24", True)
    test3 = SW_Interface("interface GigabitEthernet0/0", "static", "172.16.1.1/24", True)
    print(test3.set_switchport(True))
    r1 = R_Interfaces("R1", [])
    print(r1.interfaces)
    print(test1.ip_add)
    r1.add_interface(test1)
    test1.set_ip_add("1.1.1.1/32")
    print(test1.ip_add)
    print(test1)
    r1.add_interface(test1)
    r1.add_interface(test2)
    print(r1.interfaces[0].ip_add)
    print(r1.interfaces[1].ip_add)
    r1.interfaces[0].set_ip_add("2.2.2.1/32")
    print(r1.interfaces[0].ip_add)
    print(r1.interfaces[1].ip_add)
