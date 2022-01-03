
"""
read temaplte and return the bonus message
"""

import jinja2

template_dir = './templates'
loader = jinja2.FileSystemLoader(template_dir)
env = jinja2.Environment(loader=loader)

def bonus_template(user_id, amount, title, message):
    template = env.get_template("bonus.json")
    return template.render(user_id="111", amount='asdf',title="variables", message="here")



