import yaml

def load_inventory(file_path):
    """
    Load a device inventory from a YAML file.

    Args:
        file_path (str): Path to the YAML inventory file.

    Returns:
        dict: Device inventory.
    """

    try:
        with open(file_path, "r") as file: 
            inventory = yaml.safe_load(file)

        return inventory
    
    except Exception as e:
        print(f"Failed to load inventory: {e}")
        raise