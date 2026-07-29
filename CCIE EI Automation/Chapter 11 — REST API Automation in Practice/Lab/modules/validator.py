def validate_command(connection, command, expected_output):
    """
    Execute a show command and verify the expected output.

    Args:
        connection: Netmiko connection object.
        command (str): Show command.
        expected_output (str): Expected keyword.

    Returns:
        bool
    """

    try:

        output = connection.send_command(command)

        return expected_output in output

    except Exception as e:
        print(f"Validation failed: {e}")
        raise