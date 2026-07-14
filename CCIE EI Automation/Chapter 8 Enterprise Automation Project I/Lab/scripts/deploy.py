# Run this project from the project root:
#
# cd ~/automation_project
# python3 -m scripts.deploy

from modules import connection
from modules import inventory
from modules import renderer
from modules import output
from modules import deployment
from modules import validator
from modules.logger import logger


def main():
    print("=" * 60)
    print("Enterprise Automation Project")
    print("=" * 60)
    
    generated_count = 0
    validation_passed = 0
    validation_failed = 0

    # Load the device inventory
    devices = inventory.load_inventory("inventory/devices.yaml")

    for device in devices:

        # Load device configuration data
        device_data = inventory.load_inventory(
            f"inventory/{device['inventory_file']}"
        )

        # Render the Jinja2 template
        configuration = renderer.render_template(
            "main.j2",
            device_data
        )

        # Save the rendered configuration
        output_file = f"output/{device['hostname']}.cfg"
        output.save_configuration(
            output_file,
            configuration
        )

        logger.info(f"Generated {output_file}")

        # Load configuration commands
        commands = deployment.load_configuration(output_file)

        connection_device = {
            "device_type": device["device_type"],
            "host": device["host"],
            "username": device["username"],
            "password": device["password"],
}
        
        # Connect to the device
        connection_object = connection.connect_device(connection_device)

        validation_result = False

        try:
            # Deploy the configuration
            deployment.deploy_configuration(
                connection_object,
                commands
            )
        
            validation_result = validator.validate_command(
                connection_object,
                "show running-config | include hostname",
                f"hostname {device_data['hostname']}"
            )

        finally:
            # Disconnect from the device
            connection.disconnect_device(connection_object)

        if validation_result:
            validation_passed += 1
            logger.info(f"Validation passed: {device['hostname']}")
            print(f"{device['hostname']} Validation Passed")
            
        else:
            validation_failed += 1
            logger.error(f"Validation failed: {device['hostname']}")
            print(f"{device['hostname']} Validation Failed")

        generated_count += 1

        print(f"Generated {output_file}\n")

    print("=" * 60)
    print(f"Configurations Generated : {generated_count}")
    print(f"Validation Passed        : {validation_passed}")
    print(f"Validation Failed        : {validation_failed}")
    print("=" * 60)
    

if __name__ == "__main__":
    main()
    

