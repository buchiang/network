from jinja2 import Environment, FileSystemLoader

environment = Environment(
    loader=FileSystemLoader("templates")
)

template = environment.get_template(
    "hostname.j2"
)

device = {
    "host": "12.1.1.1",
    "username": "admin",
    "password": "cisco123",
    "device_type": "cisco_ios"
  }

rendered_config = template.render(device)

template.render(device)