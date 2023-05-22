# import pyats
from genie.testbed import load

tb = load("../backend/tb.yaml")

def show_command(device, command):
    device = device.upper()
    dev = tb.devices[device]
    dev.connect(log_stdout=False)
    return dev.parse(command)

# if __name__ == '__main__':
    # show_command("R2", "show ip interface brief")
