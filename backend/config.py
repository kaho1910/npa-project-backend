# loader our newly minted testbed file
from pyats.topology import loader
testbed = loader.load('device.yaml')

# access the devices
# # #testbed.devices
# AttrDict({'ios-1': <Device ott-tb1-n7k4 at 0xf77190cc>,
#           'ios-2': <Device ott-tb1-n7k5 at 0xf744e16c>})
ios_1 = testbed.devices['ios-1']

# establish basic connectivity
ios_1.connect()

# issue commands
print(ios_1.execute('show version'))
ios_1.configure('''
    interface GigabitEthernet0/0
        ip address 10.10.10.1 255.255.255.0
        no shut
''')
