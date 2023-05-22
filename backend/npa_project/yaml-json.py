import yaml
import json

def convert_yaml_to_json(yaml_file):
    try:
        with open(yaml_file, 'r') as file:
            # Load YAML data
            yaml_data = yaml.safe_load(file)
            
            # Convert YAML to JSON
            json_data = json.dumps(yaml_data, indent=4)
            
            return json_data
    except FileNotFoundError:
        print(f"File '{yaml_file}' not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {str(e)}")

# Example usage
yaml_file_path = 'my_testbed.yaml'
json_data = convert_yaml_to_json(yaml_file_path)
print(json_data)
