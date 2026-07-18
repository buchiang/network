def execute_show_command(connection, command):
    try:
        output = connection.send_command(command)
        return output
    except Exception as e:
        print(f"Failed to execute show command: {e}")
        raise

def deploy_configuration(connection, commands):
    try:
        output = connection.send_config_set(commands)
    except Exception as e:
        print(f"Failed to deploy configuration: {e}")
        raise

def load_configuration(file_path):
    try: 
        with open(file_path, "r") as file:
            commands = file.read().splitlines()
        return commands
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        raise