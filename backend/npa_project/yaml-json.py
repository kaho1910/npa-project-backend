import yaml, json

# Convert YAML file to dictionary
def yaml_to_dict(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

# Convert list to JSON file
def list_to_json(data):
    return json.dump(data, open('test.json', 'w'), indent=2)

# Path to the YAML file
yaml_file = 'my_testbed.yaml'

# Convert YAML to dictionary
data_dict = yaml_to_dict(yaml_file)

# Convert list to JSON
devices = []
for device in data_dict['devices']:
    data = data_dict['devices'][device]['custom']
    data["status"] = device_test_connection()
    devices.append(data)
    
list_to_json(devices)
print(open('test.json', 'r'))
