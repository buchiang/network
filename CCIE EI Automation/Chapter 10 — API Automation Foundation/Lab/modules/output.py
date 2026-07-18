def save_configuration(file_path, configuration):
    """
    Save the rendered configuration to a file.

    Args:
        file_path (str): Output file path.
        configuration (str): Rendered configuration.
    """

    try:
        with open(file_path, 'w') as file:
            file.write(configuration)
    
    except Exception as e:
        print(f"Failed to save configuration: {e}")
        raise