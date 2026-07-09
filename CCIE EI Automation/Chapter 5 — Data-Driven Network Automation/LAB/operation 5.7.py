
def collect_show_version(connection):
    try:
        output = connection.send_command("show version")
        return output
    except Exception as e:
        print(e)
        raise # Re-raise the exception to the caller.

def send_config_set(connection, commands):
    try:
        output = connection.send_config_set(commands)
        return output
    except Exception as e:
        print(e)
        raise
        