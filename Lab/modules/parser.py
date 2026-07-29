from pathlib import Path

def load_configuration(file_path):
    """Load a configuration file and return it as a string."""
    with open(file_path) as file:
        return file.read()


def get_hostname(config):
    """Return the configured hostname."""
    for line in config.splitlines():
        line = line.strip()

        if line.startswith("hostname "):
            return line.split()[1]

    return None


def get_ntp_servers(config):
    """Return a list of configured NTP servers."""
    ntp_servers = []

    for line in config.splitlines():
        line = line.strip()

        if line.startswith("ntp server "):
            ntp_servers.append(line.split()[2])

    return ntp_servers


def get_logging(config):
    """Return a list of configured syslog servers."""
    logging_servers = []

    for line in config.splitlines():
        line = line.strip()

        if line.startswith("logging host "):
            logging_servers.append(line.split()[2])

    return logging_servers


def get_ssh_version(config):
    """Return the configured SSH version."""
    for line in config.splitlines():
        line = line.strip()

        if line.startswith("ip ssh version "):
            return line.split()[3]

    return None


def get_password_encryption(config):
    """Return True if service password-encryption is enabled."""
    for line in config.splitlines():
        line = line.strip()

        if line == "service password-encryption":
            return True

    return False


def parse_configuration(config):
    """Parse the running configuration into a structured dictionary."""
    return {
        "hostname": get_hostname(config),
        "ntp_servers": get_ntp_servers(config),
        "logging_servers": get_logging(config),
        "ssh_version": get_ssh_version(config),
        "password_encryption": get_password_encryption(config),
    }