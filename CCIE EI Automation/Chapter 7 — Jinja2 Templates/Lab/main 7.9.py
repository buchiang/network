from jinja2 import Environment, FileSystemLoader

environment = Environment(
    loader=FileSystemLoader("templates")
)

template = environment.get_template("hostname.j2")

devices = [
    {
    "hostname": "R1",
    "interface":"Loopback0",
    "loopback_ip": "1.1.1.1",
    "subnet_mask": "255.255.255.255",
  },
{
    "hostname": "R2",
    "interface":"Loopback0",
    "loopback_ip": "2.2.2.2",
    "subnet_mask": "255.255.255.255",
  }
]

required_fields = [
    "hostname",
    "loopback_ip",
    "subnet_mask"
]

for device in devices:
    for field in required_fields:
        if field not in device:
            raise ValueError(f"Missing required field: {field}")
        else:
            render_config = template.render(device)

            with open(f"output/{device['hostname']}.cfg", 
                      "w") as file:
                    file.write(render_config)