def has_hostname(hostname):
    return hostname is not None

def has_ntp_servers(ntp_servers):
    return len(ntp_servers) > 0

def has_logging(logging_servers):
    return len(logging_servers) > 0

def is_ssh_version_2(ssh_version):
    return ssh_version == "2"

def is_password_encryption_enabled(enabled):
    return enabled