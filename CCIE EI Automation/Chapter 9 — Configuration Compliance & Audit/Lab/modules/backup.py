from pathlib import Path

def get_running_configuration(connection):
    return connection.send_command("show running-config")

def save_backup(hostname, configuration):
    backup_directory = Path("backups")
    backup_directory.mkdir(exist_ok=True)

    backup_file = backup_directory / f"{hostname}.cfg"

    with open(backup_file, "w") as file:
        file.write(configuration)

    return backup_file