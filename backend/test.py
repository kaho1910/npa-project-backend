from pyats.topology import loader

testbed = loader.load('device.yaml')

device = testbed.devices['RS']
test_device = testbed.devices['test']

config = """
no service password-encryption
!
hostname test
!
boot-start-marker
boot-end-marker
!
!
no logging console
enable secret 5 $1$XF4W$LbL2tAr3XwA2u2ox51nbc.
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
!
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
username admin privilege 15 secret 5 $1$biDn$RRfj.uS9/8P7Rs96KcRgs.
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
 ip address 172.16.2.1 255.255.255.0
 duplex auto
 speed auto
 media-type rj45
!
interface GigabitEthernet0/1
 no ip address
 shutdown
 duplex auto
 speed auto
 media-type rj45
!
interface GigabitEthernet0/2
 no ip address
 shutdown
 duplex auto
 speed auto
 media-type rj45
!
interface GigabitEthernet0/3
 ip address 10.0.15.202 255.255.255.0
 duplex auto
 speed auto
 media-type rj45
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
ip route 0.0.0.0 0.0.0.0 10.0.15.1
!
ipv6 ioam timestamp
!
!
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

test_device.connect()
test_device.configure(config)
test_device.execute("exit")
# device.connect()

# file_config = open("output/output.txt", "w")

# device.configure('''
#     interface GigabitEthernet0/3
#         description Interface G0/3 to WAN and IT-KMITL LAN
# ''')

# print(device.execute('show run | s interface GigabitEthernet0/3'), file=file_config)

# device.execute('exit')

