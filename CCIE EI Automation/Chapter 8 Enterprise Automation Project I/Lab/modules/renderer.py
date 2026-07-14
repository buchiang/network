from jinja2 import Environment, FileSystemLoader

environment = Environment(
    loader=FileSystemLoader("templates")
)

def render_template(template_name, data):
    """
    Render a Jinja2 template using the provided data.

    Args:
        template_name (str): Template filename.
        data (dict): Template variables.

    Returns:
        str: Rendered configuration.
    """

    try:
        template = environment.get_template(template_name)
        rendered_configuration = template.render(**data)
        return rendered_configuration
    
    except Exception as e:
        print(f"Failed to render template: {e}")
        raise