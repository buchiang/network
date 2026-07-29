import yaml

def load_yaml(file_path):

    try:
        with open(file_path, "r") as file: 
            load_yaml = yaml.safe_load(file)

        return load_yaml
    
    except Exception as e:
        print(f"Failed to load YAML file: {e}")
        raise