from pyats.topology import loader

testbed = loader.load('device.yaml')

device = testbed.devices['RS']
test_device = testbed.devices['test']

config = """

!
! Last configuration change at 12:41:47 UTC Mon May 22 2023 by admin
!
version 15.7
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname RS
!
boot-start-marker
boot-end-marker
!
!
no logging console
enable secret 5 $1$Crel$Ac8y2FHDpm6C3NRqore.M/
!
no aaa new-model
!
!
!
mmi polling-interval 60
no mmi auto-configure
no mmi pvc
mmi snmp-timeout 180
!
!
!
!
!
no ip icmp rate-limit unreachable
!
!
!
ip dhcp excluded-address 1.1.1.200 1.1.1.255
!
ip dhcp pool test1
 network 1.1.1.0 255.255.255.0
 default-router 1.1.1.1 
 dns-server 8.8.8.8 8.8.4.4 
 class test
  address range 1.1.1.1 1.1.1.100
!
ip dhcp pool test2
 network 2.2.2.0 255.255.255.0
 dns-server 8.8.8.8 8.8.4.4 
 default-router 2.2.2.2 
!
!
ip dhcp class test
!
!
no ip domain lookup
ip domain name npa.proj
ip cef
no ipv6 cef
!
multilink bundle-name authenticated
!
!
!
!
username admin privilege 15 secret 5 $1$BmJC$kasz2uxbd62nLfpmSFB/4.
!
redundancy
!
no cdp log mismatch duplex
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!
!
interface GigabitEthernet0/0
 description Interface G0/0 to Topology1
 ip address 172.16.1.254 255.255.255.0
 ip nat outside
 ip virtual-reassembly in
 duplex auto
 speed auto
 media-type rj45
 no cdp enable
!
interface GigabitEthernet0/1
 description Interface G0/1 to Topology2
 ip address 172.16.2.254 255.255.255.0
 ip nat outside
 ip virtual-reassembly in
 duplex auto
 speed auto
 media-type rj45
!
interface GigabitEthernet0/2
 description Interface G0/2 to Servers
 ip address 10.0.0.1 255.255.255.0
 ip nat inside
 ip virtual-reassembly in
 duplex auto
 speed auto
 media-type rj45
!
interface GigabitEthernet0/3
 description Interface G0/3 to WAN
 ip address 10.0.15.201 255.255.255.0
 ip nat outside
 ip virtual-reassembly in
 duplex auto
 speed auto
 media-type rj45
 no cdp enable
!
router ospf 1
 network 10.0.0.0 0.0.0.255 area 10
 network 172.16.2.0 0.0.0.255 area 0
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
ip nat inside source list topo1 interface GigabitEthernet0/0 overload
ip nat inside source list topo2 interface GigabitEthernet0/1 overload
ip nat inside source list wan interface GigabitEthernet0/3 overload
ip route 0.0.0.0 0.0.0.0 10.0.15.1
!
ip access-list extended topo1
 permit ip 10.0.0.0 0.0.0.255 172.16.1.0 0.0.0.255 log
 permit ip host 172.16.1.254 172.16.1.0 0.0.0.255 log
ip access-list extended topo2
 permit ip 10.0.0.0 0.0.0.255 172.16.2.0 0.0.0.255 log
 permit ip host 172.16.2.254 172.16.2.0 0.0.0.255 log
ip access-list extended wan
 deny   ip any 172.16.0.0 0.0.255.255 log
 permit ip any any log
!
ipv6 ioam timestamp
!
!
access-list 100 permit ip any any
!
control-plane
!

!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 exec-timeout 0 0
 login local
 transport input ssh
line vty 5 15
 login local
 transport input ssh
!
no scheduler allocate
!
end

"""

device.connect()
# print(device.execute('show run'), file=open("output/output.txt", "w"))
device.configure(config)
# test_device.configure(config)
# test_device.execute("write")
# test_device.execute("exit")
# device.connect()

# file_config = open("output/output.txt", "w")

# device.configure('''
#     interface GigabitEthernet0/3
#         description Interface G0/3 to WAN and IT-KMITL LAN
# ''')

# print(device.execute('show run | s interface GigabitEthernet0/3'), file=file_config)

# device.execute('exit')

