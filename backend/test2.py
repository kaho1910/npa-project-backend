from pyats.topology import loader, Interface, link
import genie

testbed = loader.load('device.yaml')

device = testbed.devices['RS']
test_device = testbed.devices['test']

interface_a = Interface('GigabitEthernet0/1', type = 'gigabitethernet', ipv4 = '172.16.2.254')
interface_b = Interface('GigabitEthernet0/0', type = 'gigabitethernet', ipv4 = '172.16.2.1')

# link = Link('gigabitethernet-1')

# device.add_interface(interface_a)
# test_device.add_interface(interface_b)

# interface_a.link = link
# interface_b.link = link

print(len(device.find_links(test_device)))
for link in device.links:
    print(repr(link))
