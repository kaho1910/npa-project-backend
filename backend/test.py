from pyats.topology import loader

testbed = loader.load('device.yaml')

device = testbed.devices['RS']
test_device = testbed.devices['test']

device.connect()

file_config = open("output/output.txt", "w")

device.configure('''
    interface GigabitEthernet0/3
        description Interface G0/3 to WAN and IT-KMITL LAN
''')

print(device.execute('show run | s interface GigabitEthernet0/3'), file=file_config)

device.execute('exit')

device.close()
