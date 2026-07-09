from netmiko import ConnectHandler

def collect_show_version(connection):
    try:
        output = connection.send_command("show version")
        return output
    except Exception as e:
        print(e)

def send_config_set(connection):
    commands = [
        "interface loopback100",
        "description Configured by Automation",
    ]

    for command in commands:
        try:
            connection.send_config_set(connection, command)
            print("Success")
        except Exception as e:
            print(e)
